"""
Use to get completions from an OpenAI completions endpoint. This version
of the script only works with Azure OpenAI service, since OpenAI no longer
hosts their code completion models.
"""
from typing import List
from multipl_e.completions import partial_arg_parser, make_main
import json
import openai
import openai.error
import os
import time
from typing import List

global engine, model


def completions(
    prompt: str, max_tokens: int, temperature: float, n: int, top_p, stop
) -> List[str]:
    while True:
        try:
            if engine is not None:
              results = openai.Completion.create(
                  engine=engine,
                  prompt=prompt,
                  temperature=temperature,
                  max_tokens=max_tokens,
                  top_p=top_p,
                  n=n,
                  stop=stop,
              )
              time.sleep(0.5)
            elif model is not None:
              results = openai.Completion.create(
                  model=model,
                  prompt=prompt,
                  temperature=temperature,
                  max_tokens=max_tokens,
                  top_p=top_p,
                  n=n,
                  stop=stop,
              )
            return [choice["text"] for choice in results["choices"]]
        except openai.error.RateLimitError:
            print("Rate limited...")
            time.sleep(5)


def main():
    global engine, model
    args = partial_arg_parser()
    args.add_argument("--model", type=str)
    args.add_argument("--engine", type=str)
    args.add_argument("--name-override", type=str)
    args.add_argument("--azure", action="store_true")
    args = args.parse_args()

    if args.engine is None and args.model is None:
        raise ValueError("Must specify either engine or model.")
    elif args.engine is not None and args.model is not None:
        raise ValueError("Must specify either engine or model, not both.")

    engine = args.engine
    model = args.model
    if args.azure:
      openai.api_type = "azure"
      openai.api_base = os.getenv("OPENAI_API_BASE")
      openai.api_version = "2022-12-01"
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if args.name_override:
        name = args.name_override
    else:
        if args.engine is not None:
            name = args.engine
        else:
            name = args.model

    make_main(args, name, completions)


if __name__ == "__main__":
    main()
