# TAPA 2.0 — duas versões da landing page

O repositório mantém um único `index.html` e `style.css`. A oferta com preço fica
entre os marcadores `variant:priced` no HTML; a oferta sem preço fica em
`variants/sem-valor.html`. Para alterar conteúdo comum, edite `index.html`;
para alterar somente a oferta sem preço, edite o fragmento da variante.
Os botões WhatsApp das duas páginas apontam para Luana, no número
`+55 45 99925-9973`, com a mensagem de interesse na inscrição. Antes de
publicar, confirme se esse contato ainda é o canal correto para a campanha.

Execute `python -m unittest discover -s tests -v` e `python scripts/build.py`.
As saídas são `dist/com-valor/` e `dist/sem-valor/`, cada qual pronta para ser
servida como site estático (com `index.html`, CSS e imagens). O diretório `dist/`
não é versionado. Para pré-visualizar localmente, use
`python -m http.server 8000 --directory dist` e abra `/com-valor/` ou
`/sem-valor/`.

## Integração e publicação

O workflow `.github/workflows/landing.yml` testa as duas versões em pull requests
e na branch `master`, gera um artefato de ambas e publica por SSH após push em
`master` somente quando a variável `DEPLOY_ENABLED` for `true`. Até configurar
o servidor, os artefatos ficam disponíveis no GitHub Actions para revisão.

Para um servidor Linux que ofereça SSH e `rsync`, configure em **Settings →
Secrets and variables → Actions → Variables**:

| Variável | Conteúdo |
| --- | --- |
| `DEPLOY_ENABLED` | `true`, somente após testar o destino |
| `DEPLOY_HOST` | Hostname ou IP do servidor |
| `DEPLOY_USER` | Usuário SSH com permissão de escrita |
| `DEPLOY_ROOT` | Diretório absoluto publicado pelo servidor web; abaixo dele serão criados `com-valor/` e `sem-valor/` |

Em **Actions → Secrets**, configure `DEPLOY_SSH_KEY` (chave privada exclusiva para
deploy) e `DEPLOY_KNOWN_HOSTS` (linha verificada da chave pública SSH do servidor).
Adicione a chave pública de deploy ao `authorized_keys` do usuário no servidor.
O domínio deve apontar para `DEPLOY_ROOT`; as URLs serão
`https://seu-dominio/com-valor/` e `https://seu-dominio/sem-valor/`.
Configure HTTPS no servidor ou proxy web. Se a hospedagem for cPanel, Portainer,
Synology ou outra sem SSH/rsync, adapte apenas o job `deploy` ao método de acesso
real antes de habilitar a publicação. Pull requests nunca recebem este deploy.
