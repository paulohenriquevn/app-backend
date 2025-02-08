# coleta-dados

Teste:
http://37.27.255.191:8000/status

Conectando:

```sh
ssh-keygen -R 37.27.255.191

ssh deploy@37.27.255.191

ssh root@37.27.255.191
```

Em caso de problema:

```sh
git clone git@github.com:paulohenriquevn/app-backend.git app-backend
```

# ✅ Passo a Passo para Resolver o Git

Siga os passos diretamente no servidor (`deploy@app-backend`).

## 1️⃣ Verifique se a chave SSH existe no servidor

Rode o seguinte comando:

```sh
ls -la ~/.ssh/
```

## 2️⃣ Se a chave SSH não existir, gere uma nova

Se os arquivos id_rsa e id_rsa.pub não existirem, crie uma nova chave SSH:

```sh
ssh-keygen -t rsa -b 4096 -C "deploy@servidor-app-backend"
```

Agora, confirme que os arquivos foram gerados:

```sh
ls -la ~/.ssh/
```

## 3️⃣ Adicione a chave pública ao GitHub

Agora, pegue a chave pública e copie seu conteúdo:

```sh
cat ~/.ssh/id_rsa.pub
```

No GitHub:
    
    Vá para GitHub → Settings → SSH and GPG Keys.
    
    Clique em New SSH Key.
    
    Cole a chave pública e dê um nome para identificá-la.
    
    Marque a opção "Allow write access" se for um repositório privado e precisar fazer push.

Agora, teste a conexão:

```sh
ssh -T git@github.com
```

docker logs app-backend