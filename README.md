# Casamento Photo Gallery

## Descrição

Aplicação web em Flask para upload, visualização, download e edição de nomes de fotos de um ensaio de casamento. Gera automaticamente thumbnails 300×300 e fornece links seguros para compartilhamento.

## Funcionalidades

- Listagem de todas as fotos disponíveis.
- Upload de novas imagens (PNG, JPG, JPEG, GIF).
- Geração automática de thumbnails em 300×300.
- Download de imagens com cache de 30 dias.
- Visualização protegida via tokens (itsdangerous).
- Renomeação de arquivos diretamente pela interface web.

## Estrutura de Pastas

```
casamento/
│
├─ app.py                # Aplicação Flask principal
├─ requirements.txt      # Dependências Python
├─ logs/
│   └─ error.log         # Log de erros
├─ static/
│   ├─ icon.ico          # Ícone do site
│   └─ photos/           # Diretório de fotos
│       └─ thumbs/       # Thumbnails gerados
└─ templates/            # Templates Jinja2
    ├─ base.html
    ├─ gallery.html
    ├─ view.html
    └─ edit.html
```

## Requisitos

- Python 3.10 ou superior
- Virtualenv (recomendado)

## Instalação

1. Clone o repositório:
   ```bash
   git clone <URL_DO_REPO>
   cd casamento
   ```
2. Crie e ative um ambiente virtual:

   Windows:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
   Linux/macOS:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Configuração

- Abra `app.py` e defina uma chave secreta forte em `app.secret_key`.
- Ajuste, se necessário, caminhos de diretório em `PHOTO_DIR` e `THUMB_DIR`.

## Executando a Aplicação

```bash
python app.py
```

Acesse `http://localhost:5000/` no navegador.

## Rotas Principais

- `/` — Galeria de fotos.
- `POST /upload` — Upload de novas imagens.
- `/download/<filename>` — Download da imagem.
- `/generate-token/<filename>` — Gera link seguro para visualização.
- `/view/<token>` — Visualiza imagem usando token.
- `/edit/<filename>` — Renomeia arquivo de imagem.

## Contribuição

1. Faça um fork do projeto.
2. Crie uma branch para sua feature (`git checkout -b feature/nome-da-feature`).
3. Faça commit das suas alterações (`git commit -m 'Descrição da feature'`).
4. Envie para o repositório original (`git push origin feature/nome-da-feature`).
5. Abra um Pull Request.

## Licença

Este projeto está licenciado sob a Licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.