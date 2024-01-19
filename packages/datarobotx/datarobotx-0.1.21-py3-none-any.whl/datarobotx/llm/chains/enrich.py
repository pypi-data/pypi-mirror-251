#
# Copyright 2023 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from __future__ import annotations

from typing import Any, Callable, cast, Dict, List, Optional, Union
import weakref

from langchain import embeddings
from langchain.cache import InMemoryCache
from langchain.chains.base import Chain
from langchain.chains.llm import LLMChain
from langchain.embeddings.base import Embeddings
from langchain.memory import ConversationBufferMemory
from langchain.prompts.base import BasePromptTemplate
from langchain.prompts.prompt import PromptTemplate
from langchain.schema.language_model import BaseLanguageModel
import pandas as pd

from datarobotx.common.logging import tqdm
from datarobotx.llm.utils import _embedding_cache, with_embedding_cache, with_llm_cache

_ENRICH_CONTEXT = (
    "A dataset is being prepared to train a predictive model. As part of "
    + "preparing the dataset new columns will be added by first retrieving an "
    + "answer to a question for each individual row in the dataset."
)

_CLASSIFY_TYPE_TEMPLATE = (
    _ENRICH_CONTEXT
    + "\n\n"
    + "State whether the answer to each question should best be represented "
    + "as a numeric, categorical, date, or free-text field for the purposes of "
    + "training a machine learning model. Your response should be one of: "
    + "numeric, categorical, date, free-text.\n\n"
    + "Question: What is the average income in zip code {{zip}}?\n"
    + "Type: numeric\n"
    + "Question: What country is {{city}} in?\n"
    + "Type: categorical\n"
    + "Question: When was {{company}} founded?\n"
    + "Type: date\n"
    + "Question: What are the main characteristics of {{product}}?\n"
    + "Type: free-text\n"
    + "Question: {question}\n"
    + "Type:\n"
)

_ENRICH_TEMPLATE = (
    _ENRICH_CONTEXT
    + "\n\n"
    + "Answer the question. Your response must be formatted as a {output_type} value that can "
    + "subsequently be used directly in training a machine learning model.\n\n"
    + "{{history}}\n"
    + "Question: {{question}}\n"
    + "Answer:\n"
)


class MLQATypeInferChain(LLMChain):
    """Infer desired datatype for subsequent ML-modeling from an LLM enrichment prompt.

    Raises
    ------
    ValueError
        If output_type inference fails

    Notes
    -----
    Required inputs for the chain are:

    question : str
        Question being posed to the LLM whose completion will be used to enrich
        the rows in a tabular dataset

    Chain output:

    output_type: str
        One of numeric, categorical, date, free-text; the appropriate data type
        for answers to the question for subsequent ML-modeling
    """

    prompt: BasePromptTemplate = PromptTemplate(
        input_variables=["question"], template=_CLASSIFY_TYPE_TEMPLATE
    )
    output_key: str = "output_type"
    default_stop: List[str] = ["\n"]

    @property
    def input_keys(self) -> List[str]:
        return ["question"]

    def prep_inputs(self, inputs: Union[Dict[str, Any], Any]) -> Dict[str, Any]:
        inputs = cast(Dict[str, Any], super().prep_inputs(inputs))
        if "stop" not in inputs:
            inputs["stop"] = self.default_stop
        return inputs

    def _validate_outputs(self, outputs: Dict[str, str]) -> None:
        super()._validate_outputs(outputs)
        if outputs[self.output_key] not in ["numeric", "categorical", "date", "free-text"]:
            raise ValueError("Unable to automatically infer enrichment output type")


def enrich(
    question: str,
    using: Union[BaseLanguageModel[Any], Chain],
    default_cache: bool = True,
    verbose: bool = False,
) -> Callable[[pd.Series[Any]], Any]:
    """Enrich structured data with completions from an LLM or chain.

    Convenience function for usage with pandas.DataFrame.apply():

    - Caches duplicative enrichment completions
    - Progress updating
    - Maps pandas row or column values to format provided question automatically
    - ML-oriented default contextual prompts and chains:
        - Attempts to infer and instruct around an appropriate completion type: numeric,
          categorical, date, or free-text
        - Prior completions included in successive prompts to encourage consistency
          (e.g. date formatting, categorical levels)
    - Customizable: interoperates with custom langchain Chains, Tools, LLMs

    Parameters
    ----------
    question : str
        Question to be answered to enrich the dataset. Provided as Python f-string that
        can be formatted with data from other fields in the dataframe row or column
    using : langchain.llms.BaseLLM or langchain.chains.base.Chain
        Langchain abstraction to be used to answer the question; if a custom chain or tool is
        provided the question will be formatted for each row/column in the DataFrame
        and then passed as the first argument when calling the chain run() method
    default_cache : bool, default = True
        If true, an InMemoryCache will be initialized and used for the lifecycle of the returned
        function; caching reduces API consumption from duplicative completions
    verbose : bool, default = False
        If True, default enrichment LLMChains will be run with verbose output

    Returns
    -------
    Callable
        Function that can be used directly by pandas.DataFrame.apply() to perform the
        requested enrichment.

    Examples
    --------
    >>> import pandas as pd
    >>> import langchain
    >>> from datarobotx.llm.chains.enrich import enrich
    >>> llm = langchain.llms.OpenAI(model_name="text-davinci-003")
    >>> df = pd.read_csv('https://s3.amazonaws.com/datarobot_public_datasets/' +
    ...                  '10K_2007_to_2011_Lending_Club_Loans_v2_mod_80.csv')
    >>> df_test = df[:5].copy(deep=True)
    >>> df_test['f500_or_gov'] = df_test.apply(enrich('Is "{emp_title}" a Fortune 500 company or ' +
    ...                                               'large government organization (Y/N)?', llm),
    ...                                        axis=1)
    """
    chain: Chain
    if isinstance(using, BaseLanguageModel):
        try:
            output_type = MLQATypeInferChain(llm=using, verbose=verbose).run(question)
            if output_type == "categorical":
                # emphasize scalar nature for llm to avoid completing all cat levels
                output_type = "single, categorical"
        except ValueError:
            output_type = "free-text"
        chain = LLMChain(
            llm=using,
            verbose=verbose,
            prompt=PromptTemplate(
                input_variables=["history", "question"],
                template=_ENRICH_TEMPLATE.format(output_type=output_type),
            ),
            memory=ConversationBufferMemory(
                memory_key="history",
                human_prefix="Question",
                ai_prefix="Answer",
            ),
            output_key="answer",
        )
    else:
        chain = using

    pbar = tqdm(
        bar_format="{n_fmt}{unit} [{elapsed}, {rate_fmt}]",
        unit=" rows",
        unit_scale=True,
        unit_divisor=1000,
    )

    @with_llm_cache(InMemoryCache() if default_cache else None)
    def enricher(s: pd.Series[Any]) -> Any:
        prompt_template = PromptTemplate.from_template(question)
        formatted_q = prompt_template.format(
            **{
                key: value
                for key, value in s.to_dict().items()
                if key in prompt_template.input_variables
            }
        )
        if isinstance(using, BaseLanguageModel):
            answer = chain(inputs={"question": formatted_q, "stop": ["\n"]})["answer"]
        else:
            answer = chain.run(formatted_q)

        pbar.update()
        return answer

    # Close progress bar when enricher function is garbage collected
    weakref.finalize(enricher, pbar.close)
    return enricher


def embed(
    text: str,
    using: Optional[Embeddings] = None,
    cache: bool = True,
) -> Callable[[Union[pd.DataFrame, pd.Series[Any]]], Any]:
    """Enrich structured data with the embeddings from an LLM or chain.

    Convenience function for usage with pandas.DataFrame.apply():

    - Caches duplicative embedding prompts
    - Progress updating

    Parameters
    ----------
    text : str
        Text to extract embedding on. Provided as Python f-string that
        can be formatted with data from other fields in the dataframe row or column
    using : langchain.embeddings.base.Embeddings, default = None
        Langchain abstraction to be used to extract embeddings
        If None, SentenceTransformerEmbeddings(model="all-MiniLM-L6-v2") will be used
    cache : bool, default = True
        If true, an InMemoryCache will be initialized and used for the lifecycle of the returned
        function; caching reduces API consumption from duplicative completions

    Returns
    -------
    Callable
        Function that can be used directly by pandas.DataFrame.apply() to perform the
        requested enrichment.

    Examples
    --------
    >>> import pandas as pd
    >>> from langchain import embeddings
    >>> embed_model = embeddings.OpenAIEmbeddings(model="text-embedding-ada-002")
    >>> df = pd.read_csv('https://s3.amazonaws.com/datarobot_public/drx/' +
    ...                  'amazon_food_reviews_small.csv')
    >>> df_test = df[:5].copy(deep=True)
    >>> df_with_embeddings = df_test.join(
    ...    df_test.apply(embed('Summary: {Summary}\nReview: {Text}', embed_model), axis=1)
    ...    )
    """
    pbar = tqdm(
        bar_format="{n_fmt}{unit} [{elapsed}, {rate_fmt}]",
        unit=" rows",
        unit_scale=True,
        unit_divisor=1000,
    )
    if using is None:
        using = embeddings.SentenceTransformerEmbeddings(model="all-MiniLM-L6-v2")
    else:
        assert isinstance(using, Embeddings)

    def embedder(s: pd.Series[Any]) -> pd.Series[Any]:
        prompt_template = PromptTemplate.from_template(text)
        formatted_q = prompt_template.format(
            **{
                key: value
                for key, value in s.to_dict().items()
                if key in prompt_template.input_variables
            }
        )

        @with_embedding_cache(cache)
        def embed(prompt: str) -> pd.Series[Any]:
            answer = pd.Series(using.embed_query(prompt))  # type: ignore[union-attr]
            answer.index = pd.Index([f"embedding_{i}" for i in range(len(answer.index))])
            return answer

        pbar.update()
        return embed(formatted_q)

    def collect_garbage() -> None:
        _embedding_cache.clear()
        pbar.close()

    # Close progress bar when embeder function is garbage collected
    weakref.finalize(embedder, collect_garbage)
    return embedder
