from __future__ import annotations

from agent_manager_runtime import AgentManagerRuntime


def main() -> None:
    runtime = AgentManagerRuntime()
    agent = runtime.create_agent()

    print("Chat agent ready. Type 'exit' to quit.")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break
        if not user_input:
            continue
        response = agent.chat(user_input)
        print(f"Assistant: {response}")


if __name__ == "__main__":
    main()
