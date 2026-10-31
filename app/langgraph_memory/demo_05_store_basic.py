from langgraph.store.memory import InMemoryStore

def main():
    store = InMemoryStore()

    tenant_id = "tenant_1"
    user_id = "u_10001"

    namespace = (tenant_id, user_id, "preferences")

    store.put(
        namespace,
        "answer_style",
        {
            "type": "preference",
            "content": "用户喜欢口语化，直接，代码完整的回答",
            "confidence": 0.95,
            "source": "user_explicit_request"
        }
    )

    item = store.get(namespace, "answer_style")

    print("get_memory")
    print(item)
    print("=" * 60)

    items = store.search(namespace)
    print("search memories")
    for memory in items:
        print("key:",memory.key)
        print("value:",memory.value)
        print("-"*60)

if __name__ == "__main__":
    main()
