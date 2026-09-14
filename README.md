# TAPA 2.0 — landing page em duas versões

O arquivo `index.html` é a fonte do conteúdo comum. O bloco com preço fica
entre os marcadores `variant:priced` no HTML; o bloco sem preço fica em
`variants/sem-valor.html`. Os botões WhatsApp apontam para Luana
(`+55 45 99925-9973`) com a mensagem de inscrição confirmada.

Execute `python -m unittest discover -s tests -v` e `python scripts/build.py`.
As saídas independentes ficam em `dist/com-valor/` e `dist/sem-valor/`.
Para pré-visualizar localmente: `python -m http.server 8000 --directory dist`;
acesse `/com-valor/` ou `/sem-valor/`.

## Portainer

O `Dockerfile` gera as duas versões e o Nginx serve:

| Caminho | Página |
| --- | --- |
| `/` | Redireciona para `/sem-valor/` |
| `/sem-valor/` | Oferta sem preço |
| `/com-valor/` | Oferta com preço original |
| `/healthz` | Resposta de saúde do contêiner |

O workflow `.github/workflows/landing.yml` testa e monta o contêiner em cada PR.
Após push em `master`, publica as tags `latest` e o SHA do commit em
`ghcr.io/cecimoura/tapavenda2.0`. Por padrão, um pacote recém-publicado no
GHCR é privado: torne-o público nas configurações do pacote **ou** configure
um registro `ghcr.io` com credencial de leitura no Portainer. Para uma página
pública, disponibilizar o pacote publicamente evita credenciais no servidor.

No Portainer, em **Stacks → Add stack → Git repository**, escolha:

1. Repositório: `https://github.com/cecimoura/TapaVenda2.0.git`;
2. Referência: `master`; Compose path: `compose.yaml`;
3. Docker Standalone (Compose), não Docker Swarm;
4. GitOps updates: escolha **Webhook** se o Portainer tiver uma URL HTTPS
   acessível ao GitHub Actions, ou **Polling** se ele ficar apenas na rede local;
   habilite **Re-pull image** nos dois casos;
5. `TAPA_HTTP_PORT` pode ser definido nas variáveis da stack. Sem ele, o
   contêiner usa a porta **8088** do host, com Nginx na porta 80 interna.

Faça o primeiro deploy somente depois que a imagem `latest` existir e estiver
acessível ao Portainer. Teste `http://IP-DO-SERVIDOR:8088/sem-valor/` e
`http://IP-DO-SERVIDOR:8088/com-valor/`. Para domínio e HTTPS, configure o proxy
reverso existente para encaminhar ao host:8088; não exponha a interface do
Portainer como se fosse a landing page.

No modo **Webhook**, habilite também **Force redeployment**, para poder repetir
um deploy mesmo quando o hash do Git ainda não tiver mudado. Depois de criar
a stack, copie a URL do **webhook GitOps** para o secret
`PORTAINER_GITOPS_WEBHOOK` do repositório, em **Settings → Secrets and variables
→ Actions**. Configure a variável `PORTAINER_ENABLED=true` somente quando a
URL for alcançável pelos runners do GitHub com TLS válido. Em cada publicação
posterior, o Actions envia o webhook **depois** de publicar a imagem. O
Portainer então busca o commit do Git e atualiza a stack com a imagem nova.
No modo **Polling**, deixe `PORTAINER_ENABLED` desativado e habilite também
**Force redeployment** junto de **Re-pull image**; um intervalo de 15 minutos
faz o Portainer buscar periodicamente a imagem nova, mesmo que o GitOps tenha
observado o commit antes do fim do build. Isso recria o contêiner a cada
intervalo, mesmo sem alteração. Se essa interrupção periódica não for
aceitável, use um runner autohospedado na rede local e o modo Webhook. Um
runner público não alcança o endereço privado do Portainer.

O pixel de marketing fica para uma alteração posterior, após testar o domínio
final e a navegação mobile.
