from langchain.text_splitter import Language

# we are only documenting the file that ends with the following extensions:
ALLOWED_EXTENSIONS = [".js", ".go", ".php", ".py", ".ts", ".tsx"]
ALLOWED_NO_CODE_EXTENSIONS = ["", ".sh", ".xml", ".yaml", ".yml"]

# split code files according the programming language
LANGUAGES = {
    ".php": Language.PHP,
    ".py": Language.PYTHON,
    ".go": Language.GO,
    ".js": Language.JS,
    ".ts": Language.JS,
    ".tsx": Language.JS,
}

DOCSTRING_LABEL = "@DEVTALE-GENERATED:"

# Extracted from https://openai.com/pricing on January 15th, 2024.
GPT_PRICE = {
    "gpt-4-1106-preview": 0.01,
    "gpt-3.5-turbo-16k": 0.0010,
    "gpt-3.5-turbo": 0.0010,
}
