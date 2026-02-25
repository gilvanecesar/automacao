# Automação RD Station - WhatsApp

Automação para envio de mensagens de saudação via WhatsApp para leads no RD Station CRM.

## 📋 Pré-requisitos

- Python 3.7 ou superior
- Google Chrome instalado
- Conta no RD Station CRM
- WhatsApp Web configurado

## 🚀 Instalação

1. **Instale as dependências:**
```bash
pip install -r requirements.txt --break-system-packages
```

2. **Ou instale manualmente:**
```bash
pip install selenium webdriver-manager --break-system-packages
```

## 📖 Como usar

1. **Execute o script:**
```bash
python rdstation_whatsapp_automation.py
```

2. **Siga os passos:**
   - O navegador Chrome abrirá automaticamente
   - Faça login no RD Station se necessário
   - Faça login no WhatsApp Web se necessário
   - O script começará a processar os leads

3. **O que o script faz:**
   - ✅ Busca leads na coluna "Entrada de Leads"
   - ✅ Verifica se o lead tem WhatsApp disponível
   - ✅ Abre o WhatsApp Web
   - ✅ Envia a mensagem de saudação
   - ✅ Muda o status para "Contato Realizado"
   - ✅ Passa para o próximo lead

## 📝 Mensagem enviada

```
Olá tudo bem? 
Me chamo Gilvane, faço parte do time de vendas da QUERO TRUCK. 
Vi que entrou em contato conosco, o que vc procura? Compra, venda de caminhões?
```

## ⚙️ Personalização

Para alterar a mensagem, edite a variável `mensagem_padrao` no arquivo:

```python
self.mensagem_padrao = """Sua mensagem aqui"""
```

## 🔧 Solução de problemas

### Erro ao encontrar elementos
- **Problema:** Os seletores CSS/XPath podem mudar se o RD Station atualizar a interface
- **Solução:** Pode ser necessário ajustar os seletores no código

### WhatsApp não conecta
- **Problema:** WhatsApp Web não está autenticado
- **Solução:** Abra https://web.whatsapp.com manualmente e escaneie o QR code

### Login não funciona
- **Problema:** Captcha ou verificação de segurança
- **Solução:** O script aguarda você fazer login manualmente

### Navegador fecha sozinho
- **Problema:** ChromeDriver incompatível
- **Solução:** Atualize o Chrome ou use webdriver-manager

## 📌 Observações importantes

- ⚠️ O script processa **um lead por vez** para evitar bloqueios
- ⚠️ Apenas leads com **botão WhatsApp disponível** serão processados
- ⚠️ Leads sem WhatsApp serão **pulados automaticamente**
- ⚠️ O script aguarda sua confirmação entre cada lead

## 🛡️ Segurança

- Mantenha suas credenciais seguras
- Não compartilhe seu código com dados sensíveis
- Use o script de acordo com os Termos de Uso do RD Station e WhatsApp

## 🐛 Ajustes necessários

Como não tenho acesso direto ao RD Station, alguns seletores podem precisar de ajustes:

1. **Seletores dos cards de leads** (linha ~90)
2. **Seletor do botão WhatsApp** (linha ~140)
3. **Mudança de status** (linha ~240) - pode precisar de ajuste manual

Se algo não funcionar, me avise com prints da tela e do erro que vou ajustar!

## 📞 Suporte

Se encontrar problemas:
1. Tire prints do erro no terminal
2. Tire prints da tela do RD Station
3. Me envie para ajustar o código

---

**Desenvolvido com ❤️ usando Python + Selenium**
