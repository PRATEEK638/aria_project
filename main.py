from ai import get_plan
import tools


def execute(action, args):
    try:
        # 🔒 Safety check
        if not isinstance(args, list):
            args = []

        if action == "create_folder":
            if len(args) < 1:
                return "❌ Missing folder path"
            return tools.create_folder(args[0])

        elif action == "create_file":
            if len(args) < 1:
                return "❌ Missing file path"
            return tools.create_file(args[0])

        elif action == "move":
            if len(args) < 2:
                return "❌ Missing source or destination"
            return tools.move(args[0], args[1])

        elif action == "delete":
            if len(args) < 1:
                return "❌ Missing path"
            confirm = input("⚠️ Confirm delete (yes/no): ")
            if confirm.lower() == "yes":
                return tools.delete(args[0])
            return "Cancelled"

        elif action == "open":
            if len(args) < 1:
                return "❌ Missing file/app name"
            return tools.open_item(args[0])

        elif action == "list":
            if len(args) < 1:
                return "❌ Missing path"
            return tools.list_files(args[0])

        else:
            return "❌ AI did not understand command"

    except Exception as e:
        return f"❌ Error: {e}"


def main():
    print("ARIA AI File Manager")
    print("Type 'exit' to quit\n")

    while True:
        cmd = input("You: ").strip()

        if not cmd:
            continue

        if cmd.lower() == "exit":
            break

        # 🧠 Get AI plan
        plan = get_plan(cmd)
        action = plan.get("action", "unknown")
        args = plan.get("args", [])
        if action == "unknown":
            from ai import chat_response
            reply = chat_response(cmd)
            print("AI:", reply)
            continue

        print(f"AI → {action} {args}")

        # ⚙️ Execute action
        result = execute(action, args)

        print(result)


if __name__ == "__main__":
    main()