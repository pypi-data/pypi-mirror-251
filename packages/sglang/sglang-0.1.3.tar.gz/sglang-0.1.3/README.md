# SGLang

SGLang is a structured generation language designed for large language models (LLMs).
It makes your interaction with LLMs faster and more controllable by co-designing the frontend language and the runtime system.

The core features of SGLang include:
- **A Flexible Front-End Language**: This allows for easy programming of LLM applications with multiple chained generation calls, advanced prompting techniques, control flow, multiple modalities, parallelism, and external interaction.
- **A High-Performance Runtime with RadixAttention**: This feature significantly accelerates the execution of complex LLM programs by automatic KV cache reuse across multiple calls. It also supports other common techniques like continuous batching and tensor parallelism.

## Contents
- [Install](#install)
- [Quick Start](#quick-start)
- [Frontend: Structured Generation Langauge (SGLang)](#frontend-structured-generation-langauge-sglang)
- [Backend: SGLang Runtime (SRT)](#backend-sglang-runtime-srt)
- [Benchmark And Performance](#benchmark-and-performance)
- [Roadmap](#roadmap)
- [Citation And Acknowledgment](#citation-and-acknowledgment)

## Install

### Method 1: With pip
```
pip install "sglang[all]"
```

### Method 2: From source
```
git clone git@github.com:sgl-project/sglang.git
cd sglang

pip install --upgrade pip
pip install -e "python[all]"
```

## Quick Start
The example below shows how to use sglang to answer a mulit-turn question.

### Using OpenAI Models
```python
from sglang import function, system, user, assistant, gen, set_default_backend, OpenAI

@function
def multi_turn_question(s, question_1, question_2):
    s += system("You are a helpful assistant.")
    s += user(question_1)
    s += assistant(gen("answer_1", max_tokens=256))
    s += user(question_2)
    s += assistant(gen("answer_2", max_tokens=256))

set_default_backend(OpenAI("gpt-3.5-turbo"))

state = multi_turn_question.run(
    question_1="What is the capital of the United States?",
    question_2="List two local attractions.",
)

for m in state.messages():
    print(m["role"], ":", m["content"])
```

### Using Local Models
First, launch a server with
```
python -m sglang.launch_server --model-path meta-llama/Llama-2-7b-chat-hf --port 30000
```

Then, connect to the server and answer a multi-turn question.

```python
from sglang import function, system, user, assistant, gen, set_default_backend, RuntimeEndpoint

@function
def multi_turn_question(s, question_1, question_2):
    s += system("You are a helpful assistant.")
    s += user(question_1)
    s += assistant(gen("answer_1", max_tokens=256))
    s += user(question_2)
    s += assistant(gen("answer_2", max_tokens=256))

set_default_backend(RuntimeEndpoint("http://localhost:30000"))

state = multi_turn_question.run(
    question_1="What is the capital of the United States?",
    question_2="List two local attractions.",
)

for m in state.messages():
    print(m["role"], ":", m["content"])
```

### More Examples

You can find more examples at [examples/quick_start](examples/quick_start).

## Frontend: Structured Generation Langauge (SGLang)

To begin with, import sglang.
```python
import sglang as sgl
```

`sglang` provides some simple primitives such as `gen`, `select`, `fork`.
You can implement your prompt flow in a function decorated by `sgl.function`.
You can then invoke the function with `run` or `run_batch`.
The system will manage the state, chat template, and parallelism for you.

### Control Flow
```python
@sgl.function
def control_flow(s, question):
    s += "To answer this question: " + question + ", "
    s += "I need to use a " + sgl.gen("tool", choices=["calculator", "web browser"]) + ". "

    # You can use if or nested function calls
    if s["tool"] == "calculator":
        s += "The math expression is" + sgl.gen("expression")
    elif s["tool"] == "web browser":
        s += "The website url is" + sgl.gen("url")
```

### Parallelism
```python
@sgl.function
def tip_suggestion(s):
    s += (
        "Here are two tips for staying healthy: "
        "1. Balanced Diet. 2. Regular Exercise.\n\n"
    )

    forks = s.fork(2)  # Launch parallel prompts
    for i, f in enumerate(forks):
        f += f"Now, expand tip {i+1} into a paragraph:\n"
        f += sgl.gen(f"detailed_tip", max_tokens=256, stop="\n\n")

    s += "Tip 1:" + forks[0]["detailed_tip"] + "\n"
    s += "Tip 2:" + forks[1]["detailed_tip"] + "\n"
    s += "In summary" + sgl.gen("summary")
```

### Multi Modality
```python
@sgl.function
def image_qa(s, image_file, question):
    s += sgl.user(sgl.image(image_file) + question)
    s += sgl.assistant(sgl.gen("answer", max_tokens=256)
```

### Constrained Decoding
```python
@function
def regular_expression_gen(s):
    s += "Q: What is the IP address of the Google DNS servers?\n"
    s += "A: " + gen(
        "answer",
        temperature=0,
        regex=r"((25[0-5]|2[0-4]\d|[01]?\d\d?).){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)",
    )
```

### Batching
```python
@sgl.function
def text_qa(s, question):
    s += "Q: " + question + "\n"
    s += "A:" + sgl.gen("answer", stop="\n")

states = text_qa.run_batch(
    [
        {"question": "What is the capital of the United Kingdom?"},
        {"question": "What is the capital of France?"},
        {"question": "What is the capital of Japan?"},
    ],
)
```

### Streaming
```python
@sgl.function
def text_qa(s, question):
    s += "Q: " + question + "\n"
    s += "A:" + sgl.gen("answer", stop="\n")

states = text_qa.run(
    question="What is the capital of France?",
    temperature=0.1)

for out in state.text_iter():
    print(out, end="", flush=True)
```

## Backend: SGLang Runtime (SRT)
The SGLang Runtime (SRT) is designed to work best with the SGLang frontend.
However, it can also be used as a standalone API server.
In this case, the RadixAttention can still greatly accelerate many use cases.

### Usage
Launch a server
```
python -m sglang.launch_server --model-path meta-llama/Llama-2-7b-chat-hf --port 30000
```

Send a request
```
curl http://localhost:30000/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Say this is a test",
    "max_tokens": 16,
    "temperature": 0
  }'
```

### Additional Arguments
- Add `--tp 2` to enable tensor parallelism.
```
python -m sglang.launch_server --model-path meta-llama/Llama-2-7b-chat-hf --port 30000 --tp 2
```

### Supported Models
- Llama
- Mistral
- Mixtral
- LLaVA
  - `python3 -m sglang.launch_server --model-path liuhaotian/llava-v1.5-7b --tokenizer-path llava-hf/llava-1.5-7b-hf --port 30000`

## Benchmark And Performance

- Llama-7B on NVIDIA A10G, FP16, Tensor Parallelism=1
![llama_7b](assets/llama_7b.jpg)

- Mixtral-8x7B on NVIDIA A10G, FP16, Tensor Parallelism=8
![mixtral_8x7b](assets/mixtral_8x7b.jpg)

Learn more [here]().

## Roadmap
- [ ] Function call
- [ ] Quantization
- [ ] S-LoRA
- [ ] More models

## Citation And Acknowledgment
```
@misc{zheng2023efficiently,
      title={Efficiently Programming Large Language Models using SGLang},
      author={Lianmin Zheng and Liangsheng Yin and Zhiqiang Xie and Jeff Huang and Chuyue Sun and Cody Hao Yu and Shiyi Cao and Christos Kozyrakis and Ion Stoica and Joseph E. Gonzalez and Clark Barrett and Ying Sheng},
      year={2023},
      eprint={2312.07104},
      archivePrefix={arXiv},
      primaryClass={cs.AI}
}
```

We learned from the design and reused some code of the following projects: [Guidance](https://github.com/guidance-ai/guidance), [vLLM](https://github.com/vllm-project/vllm), [LightLLM](https://github.com/ModelTC/lightllm), [FlashInfer](https://github.com/flashinfer-ai/flashinfer), [Outlines](https://github.com/outlines-dev/outlines), [LMQL](https://github.com/eth-sri/lmql).
