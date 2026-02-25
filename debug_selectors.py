"""
Script auxiliar para identificar seletores corretos no RD Station
Use este script para descobrir os seletores CSS/XPath corretos dos elementos
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def main():
    print("""
    ╔══════════════════════════════════════════════════════╗
    ║   HELPER - Identificador de Seletores RD Station    ║
    ╚══════════════════════════════════════════════════════╝
    
    Este script vai te ajudar a identificar os seletores corretos.
    """)
    
    # Inicia navegador
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    
    try:
        # Acessa RD Station
        print("\n1️⃣  Abrindo RD Station...")
        driver.get("https://crm.rdstation.com/app/deals/pipeline")
        
        input("\n👉 Faça login e pressione ENTER para continuar...")
        
        print("\n2️⃣  Analisando página...")
        time.sleep(2)
        
        # Tenta encontrar cards de diferentes formas
        print("\n📋 TENTANDO ENCONTRAR CARDS DE LEADS:\n")
        
        # Método 1
        print("Método 1: Buscando por elementos com 'card' no class...")
        cards_1 = driver.find_elements(By.CSS_SELECTOR, "[class*='card']")
        print(f"   Encontrados: {len(cards_1)} elementos")
        
        # Método 2
        print("\nMétodo 2: Buscando por elementos com 'deal' no class...")
        cards_2 = driver.find_elements(By.CSS_SELECTOR, "[class*='deal']")
        print(f"   Encontrados: {len(cards_2)} elementos")
        
        # Método 3
        print("\nMétodo 3: Buscando por nomes visíveis...")
        try:
            # Nomes que vemos nos prints: "Fabiano Eliseu", "Jaelson", "alanna cristina"
            nomes = driver.find_elements(By.XPATH, "//*[contains(text(), 'Fabiano') or contains(text(), 'Jaelson') or contains(text(), 'alanna')]")
            print(f"   Encontrados: {len(nomes)} nomes")
            if nomes:
                for nome in nomes[:3]:
                    print(f"      - {nome.text}")
                    print(f"        Tag: {nome.tag_name}, Class: {nome.get_attribute('class')}")
        except Exception as e:
            print(f"   Erro: {e}")
        
        # Método 4
        print("\nMétodo 4: Buscando pela coluna 'Entrada de Leads'...")
        try:
            coluna = driver.find_element(By.XPATH, "//*[contains(text(), 'Entrada de Leads')]")
            print(f"   ✅ Coluna encontrada!")
            print(f"   Tag: {coluna.tag_name}, Class: {coluna.get_attribute('class')}")
            
            # Tenta pegar o pai/container
            pai = coluna.find_element(By.XPATH, "./..")
            print(f"   Pai - Tag: {pai.tag_name}, Class: {pai.get_attribute('class')}")
            
            # Busca cards dentro deste container
            cards_coluna = pai.find_elements(By.XPATH, ".//*[contains(@class, 'card') or contains(@class, 'deal')]")
            print(f"   Cards na coluna: {len(cards_coluna)}")
            
        except Exception as e:
            print(f"   Erro: {e}")
        
        print("\n" + "="*60)
        input("\n👉 Agora, CLIQUE EM UM LEAD e pressione ENTER...")
        
        print("\n3️⃣  Analisando página do lead...")
        time.sleep(2)
        
        # Procura botão WhatsApp
        print("\n📱 PROCURANDO BOTÃO WHATSAPP:\n")
        
        try:
            # Procura pelo texto/title "Abrir com WhatsApp"
            elementos_whats = driver.find_elements(By.XPATH, "//*[contains(text(), 'Abrir com WhatsApp')]")
            
            if elementos_whats:
                print(f"✅ Encontrados {len(elementos_whats)} elementos com 'Abrir com WhatsApp'")
                
                for i, elem in enumerate(elementos_whats, 1):
                    print(f"\n   Elemento {i}:")
                    print(f"   Tag: {elem.tag_name}")
                    print(f"   Class: {elem.get_attribute('class')}")
                    print(f"   Texto: {elem.text}")
                    
                    # Mostra hierarquia (pais)
                    print(f"   Hierarquia de pais:")
                    elemento_atual = elem
                    for nivel in range(5):
                        try:
                            elemento_atual = elemento_atual.find_element(By.XPATH, "..")
                            print(f"      Nível {nivel+1}: <{elemento_atual.tag_name}> class='{elemento_atual.get_attribute('class')}'")
                            if elemento_atual.tag_name in ['button', 'a']:
                                print(f"         👆 ESTE É O ELEMENTO CLICÁVEL!")
                                break
                        except:
                            break
            else:
                print("❌ Nenhum elemento encontrado com o texto 'Abrir com WhatsApp'")
                
        except Exception as e:
            print(f"❌ Erro: {e}")
        
        # Procura abas de status
        print("\n📑 PROCURANDO ABAS DE STATUS:\n")
        
        try:
            # Procura por elementos que contenham "Contato Realizado"
            abas = driver.find_elements(By.XPATH, "//*[contains(text(), 'Contato Realizado')]")
            print(f"Encontradas {len(abas)} abas/elementos com 'Contato Realizado'")
            
            for i, aba in enumerate(abas, 1):
                print(f"\n   Elemento {i}:")
                print(f"   Tag: {aba.tag_name}")
                print(f"   Class: {aba.get_attribute('class')}")
                print(f"   Texto: {aba.text}")
                print(f"   Clicável: {aba.is_enabled()}")
        except Exception as e:
            print(f"Erro: {e}")
        
        print("\n" + "="*60)
        print("\n✅ Análise concluída!")
        print("\n💡 PRÓXIMOS PASSOS:")
        print("   1. Copie as informações acima")
        print("   2. Me envie para ajustar os seletores no script")
        print("   3. Teste novamente com os seletores corretos")
        
        input("\nPressione ENTER para fechar...")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
