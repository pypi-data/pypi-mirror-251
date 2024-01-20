"""
InterLab core
-------------

Core functionality of InterLab:
* `tracing` with rich structured logging of nested `TraceNode`s, storage for tracing nodes, and custom-visualized
  content (Images, generic HTML, and f-strings visualizing the field substitutions)
* `actor` for `ActorBase` and few basic agents (including a generic LLM agent and a web console for playing
  as an actor yourself), and actor memory system.
* `lang_models` with several LLM APIs, web-console "LLM" for debugging, and generic wrapper `query_model`
  unifying API of our models, LangChain models (both chat and non-chat models) and general callable functions,
  while doing tracing logging.
* `queries` holds powerful helpers for advanced queries to the models: querying the model for structured
  data for any dataclass or Pydantic model, including generating schemas, optionally generating examples, and
  robust and powerful response parsing for JSON (with repeats and validation).
* `ui` contains the server for tracing browser and the web consoles (actor and model), along with compiled web apps.
* `utils` with several text utilities, color handling and other helpers.

And finally, `ext` contains extensions and integrations with other systems (currently Matplotlib and Google Colab).

Note that this package does not contain more complex and concrete implementations of actors, scenarios, and other
LLM-based algorithms. You can find a growing collection of these in `interlab_zoo`.
"""

from . import actor, environment, queries, utils
from .__version__ import __version__

__all__ = ["actor", "environment", "queries", "utils", "__version__"]
