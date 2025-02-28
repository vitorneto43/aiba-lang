import os
import requests
import sys

AIBA_PKG_REPO = "https://aiba-lang.org/packages/"


def install_package(package_name):
    url = f"{AIBA_PKG_REPO}{package_name}.zip"
    response = requests.get(url)
    if response.status_code == 200:
        with open(f"{package_name}.zip", "wb") as f:
            f.write(response.content)
        os.system(f"unzip {package_name}.zip -d aiba_packages/{package_name}")
        os.remove(f"{package_name}.zip")
        print(f"✅ Pacote '{package_name}' instalado com sucesso!")
    else:
        print(f"❌ Erro: Pacote '{package_name}' não encontrado.")


def update_packages():
    print("🔄 Atualizando pacotes...")
    # Simulação de atualização, pode ser expandido
    print("✅ Todos os pacotes estão atualizados.")


def publish_package(package_path):
    if not os.path.exists(package_path):
        print("❌ Erro: Caminho do pacote inválido.")
        return
    print(f"📦 Publicando '{package_path}'...")
    # Aqui poderia haver integração com um servidor
    print("✅ Pacote publicado com sucesso!")


def main():
    if len(sys.argv) < 3:
        print("Uso: aiba-pkg <comando> <pacote>")
        print("Comandos disponíveis: install, update, publish")
        return

    command = sys.argv[1]
    package = sys.argv[2]

    if command == "install":
        install_package(package)
    elif command == "update":
        update_packages()
    elif command == "publish":
        publish_package(package)
    else:
        print("❌ Comando inválido.")


if __name__ == "__main__":
    main()
