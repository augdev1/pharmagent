import argparse
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv


def run_command(command, cwd):
    result = subprocess.run(command, cwd=cwd)
    if result.returncode != 0:
        sys.exit(result.returncode)


def main():
    parser = argparse.ArgumentParser(
        description="Inicialização rápida do Pharma Agent (equivalente a npm run dev)."
    )
    parser.add_argument("--host", default="127.0.0.1", help="Host do Django runserver")
    parser.add_argument("--port", default="8000", help="Porta do Django runserver")
    parser.add_argument(
        "--no-migrate",
        action="store_true",
        help="Não executa migrations antes de subir o servidor",
    )
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parent
    manage_py = project_root / "agnoframework" / "manage.py"

    if not manage_py.exists():
        print("Erro: arquivo manage.py não encontrado em agnoframework/manage.py")
        sys.exit(1)

    load_dotenv(project_root / ".env")

    print("Iniciando Pharma Agent em modo DEV...")

    if not args.no_migrate:
        print("Aplicando migrations...")
        run_command([sys.executable, str(manage_py), "migrate"], cwd=project_root)

    print(f"Subindo servidor em http://{args.host}:{args.port}/")
    run_command(
        [sys.executable, str(manage_py), "runserver", f"{args.host}:{args.port}"],
        cwd=project_root,
    )


if __name__ == "__main__":
    main()
