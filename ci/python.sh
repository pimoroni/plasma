QA_SCRIPT_PATH=${BASH_SOURCE-$0}
QA_SCRIPT_PATH=$(dirname "$QA_SCRIPT_PATH")
QA_SCRIPT_PATH=$(realpath "$QA_SCRIPT_PATH")

function qa_prepare_all {
    pip install ruff
}

function qa_check {
    ruff check --config "$QA_SCRIPT_PATH/ruff.toml" "$1"
}

function qa_fix {
    ruff check --config "$QA_SCRIPT_PATH/ruff.toml" --fix "$1"
}

function qa_examples_check {
    qa_check examples/
}

function qa_examples_fix {
    qa_fix examples/
}

function qa_modules_check {
    qa_check modules/
}

function qa_modules_fix {
    qa_fix modules/
}
