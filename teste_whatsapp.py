"""
Script de TESTE - Envio de mensagem WhatsApp
Usa para testar se consegue enviar mensagem no WhatsApp Web
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

def testar_whatsapp():
    print("="*60)
    print("TESTE DE ENVIO DE MENSAGEM WHATSAPP")
    print("="*60)
    
    # Abre navegador
    print("\n1. Abrindo navegador...")
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 20)
    
    try:
        # Abre WhatsApp Web
        print("2. Abrindo WhatsApp Web...")
        driver.get("https://web.whatsapp.com")
        
        input("\n👉 Faça login no WhatsApp Web (escaneie QR code) e pressione ENTER...")
        
        # Pede o número para testar
        numero = input("\n👉 Digite o número de telefone para testar (com DDD, sem espaços): ")
        
        print(f"\n3. Abrindo conversa com {numero}...")
        driver.get(f"https://web.whatsapp.com/send?phone=55{numero}")
        
        print("4. Aguardando página carregar (10 segundos)...")
        time.sleep(10)
        
        # Verifica se tem erro
        print("\n5. Verificando se número é válido...")
        try:
            erro = driver.find_elements(By.XPATH, 
                "//*[contains(text(), 'inválido') or contains(text(), 'invalid')]")
            
            if erro:
                print("❌ ERRO: Número inválido ou não existe no WhatsApp!")
                
                # Procura botão OK
                try:
                    ok_button = driver.find_element(By.XPATH, "//button[contains(text(), 'OK')]")
                    print("   Botão OK encontrado. Clicando...")
                    ok_button.click()
                    time.sleep(2)
                except:
                    print("   Botão OK não encontrado")
                
                input("\nPressione ENTER para fechar...")
                return
        except:
            pass
        
        print("✅ Número parece válido!")
        
        # Tenta encontrar a caixa de mensagem
        print("\n6. Procurando caixa de mensagem...")
        
        # Método 1
        try:
            print("   Tentando seletor 1: div[contenteditable='true'][data-tab='10']")
            caixa = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//div[@contenteditable='true'][@data-tab='10']")
            ))
            print("   ✅ ENCONTROU com seletor 1!")
        except:
            print("   ❌ Seletor 1 falhou")
            
            # Método 2
            try:
                print("   Tentando seletor 2: CSS selector")
                caixa = wait.until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "div[contenteditable='true'][data-tab='10']")
                ))
                print("   ✅ ENCONTROU com seletor 2!")
            except:
                print("   ❌ Seletor 2 falhou")
                
                # Método 3 - mais genérico
                try:
                    print("   Tentando seletor 3: qualquer div contenteditable")
                    caixa = wait.until(EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "div[contenteditable='true']")
                    ))
                    print("   ✅ ENCONTROU com seletor 3!")
                except:
                    print("   ❌ Todos os seletores falharam!")
                    print("\n💡 A página do WhatsApp pode ter mudado.")
                    print("   Tire um print e me mande!")
                    input("\nPressione ENTER para fechar...")
                    return
        
        # Clica na caixa
        print("\n7. Clicando na caixa de mensagem...")
        caixa.click()
        time.sleep(1)
        
        # Mensagem de teste
        mensagem = """Olá tudo bem? 
Me chamo Gilvane, faço parte do time de vendas da QUERO TRUCK. 
Vi que entrou em contato conosco, o que vc procura? Compra, venda de caminhões?"""
        
        print("\n8. Digitando mensagem...")
        linhas = mensagem.split('\n')
        for i, linha in enumerate(linhas):
            caixa.send_keys(linha)
            if i < len(linhas) - 1:
                caixa.send_keys(Keys.SHIFT + Keys.ENTER)
            print(f"   Linha {i+1} digitada")
        
        print("\n9. Mensagem digitada! Verificando...")
        time.sleep(2)
        
        resposta = input("\n👉 A mensagem apareceu na caixa? (s/n): ").lower()
        
        if resposta == 's':
            print("\n✅ SUCESSO! A mensagem foi digitada corretamente!")
            
            enviar = input("\n👉 Quer enviar a mensagem? (s/n): ").lower()
            if enviar == 's':
                print("10. Enviando mensagem...")
                caixa.send_keys(Keys.ENTER)
                print("✅ ENVIADO!")
                time.sleep(3)
            else:
                print("Mensagem não enviada (cancelado pelo usuário)")
        else:
            print("\n❌ A mensagem não apareceu na caixa.")
            print("💡 Problema identificado: o script não consegue digitar na caixa do WhatsApp")
            print("   Possíveis causas:")
            print("   - Seletor incorreto")
            print("   - WhatsApp mudou a interface")
            print("   - Elemento não está focado")
        
        input("\nPressione ENTER para fechar...")
        
    finally:
        driver.quit()
        print("\n✅ Navegador fechado")

if __name__ == "__main__":
    testar_whatsapp()
