# Contributing to the Antigravity Science Plugin & Custom Plugin Cookbook

Contributions, new domain skills (`SKILL.md`), custom MCP servers (`mcp_config.json`), and scientific workflow examples are welcome! This guide follows the structure and conventions of the official [Google Gemini API Cookbook (`google-gemini/cookbook`)](https://github.com/google-gemini/cookbook/blob/main/CONTRIBUTING.md).

## Style Guides & Conventions

Before submitting a pull request, please review:
* **[Google Developer Documentation Style Guide Highlights](https://developers.google.com/style/highlights):** Use second person (`"you"` rather than `"we"`), sentence case in headings, and imperative instructions (`"Run the validator script"`).
* **[Google Python Style Guide](https://google.github.io/styleguide/pyguide.html):** All helper scripts inside `skills/<skill-name>/scripts/*.py` must include [PEP 723 inline script metadata](https://peps.python.org/pep-0723/) (`# /// script`) so they can be executed deterministically via `uv run` with zero global `pip install` pollution.

## How to Add a New Custom Plugin or Scientific Skill

1. **Scaffold Your Plugin Bundle:**
   Use the built-in scaffolder to generate a compliant directory structure (`plugin.json`, `assets/logo.svg`, `rules/AGENTS.md`, `hooks.json`, `SKILL.md`, and a PEP 723 `scripts/run_tool.py` CLI script):
   ```bash
   uv run examples/scaffold_custom_plugin.py \
     --scaffold <your-plugin-name> \
     --skill <your-skill-name> \
     --description "One-line description of what your scientific or engineering plugin does."
   ```

2. **Validate Against Google Antigravity Loader Rules:**
   Every plugin in `plugins/` must pass the automated loader check (`<= 24,000`-byte rule cap, valid `plugin.json` manifest keys, root `hooks.json` placement, and valid `SKILL.md` YAML frontmatter):
   ```bash
   uv run examples/scaffold_custom_plugin.py --validate plugins/<your-plugin-name>
   ```

3. **Zero-Leak Credential & Reproducibility Standards:**
   * Never hardcode API keys or print secret environment variables to `stdout`. Follow the exit-code verification pattern in [`skills/credentials`](./DEVTO_ANTIGRAVITY_SCIENCE_PLUGIN_GUIDE.md#pattern-3-the-zero-leak-credential-protocol-skillscredentialsskillmd).
   * Ensure any CLI script supports a `--self-test` or sample input mode so automated CI and reviewers can verify the output deterministically.

4. **Open an Issue or Pull Request:**
   * File an [Issue](https://github.com/RobinaMirbahar/antigravity-science-plugin-cookbook/issues) or submit a [Pull Request](https://github.com/RobinaMirbahar/antigravity-science-plugin-cookbook/pulls) with the output of `uv run examples/scaffold_custom_plugin.py`.

## Upstream Google Ecosystem References

* **Google:** [github.com/google (`@google`)](https://github.com/google) | [about.google](https://about.google/)
* **Google Gemini API & Cookbook:** [github.com/google-gemini (`@google-gemini`)](https://github.com/google-gemini) | [google-gemini/cookbook](https://github.com/google-gemini/cookbook) | [ai.google.dev/gemini-api/docs](https://ai.google.dev/gemini-api/docs)
* **Google DeepMind Science & Models:** [github.com/google-deepmind (`@google-deepmind`)](https://github.com/google-deepmind) | [AlphaGenome](https://deepmind.google.com/science/alphagenome/) | [AlphaFold](https://alphafold.ebi.ac.uk/) | [Aeneas & Ithaca](https://predictingthepast.com/)
* **Google Antigravity Platform:** [antigravity.google/docs](https://antigravity.google/docs) | [antigravity.google/use-cases/science](https://antigravity.google/use-cases/science) | [github.com/google-antigravity (`@google-antigravity`)](https://github.com/google-antigravity/antigravity-sdk-python)
* **Google Cloud Platform:** [github.com/GoogleCloudPlatform (`@GoogleCloudPlatform`)](https://github.com/GoogleCloudPlatform) | [GoogleCloudPlatform/generative-ai](https://github.com/GoogleCloudPlatform/generative-ai)
