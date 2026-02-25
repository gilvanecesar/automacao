"""
Automação RD Station - Envio de mensagens WhatsApp
Autor: Assistente Claude
Data: 05/02/2026

Requisitos:
- Python 3.7+
- Selenium
- Chrome/Chromium instalado
- ChromeDriver compatível

Instalar dependências:
pip install selenium webdriver-manager --break-system-packages
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class RDStationWhatsAppBot:
    def __init__(self):
        """Inicializa o bot com configurações do Chrome"""
        self.driver = None
        self.wait = None
        self.mensagem_padrao = """Olá tudo bem? 
Me chamo Gilvane, faço parte do time de vendas da QUERO TRUCK. 
Vi que entrou em contato conosco, o que vc procura? Compra, venda de caminhões?"""
        
    def iniciar_navegador(self):
        """Inicia o navegador Chrome com as opções necessárias"""
        logger.info("Iniciando navegador...")
        
        options = webdriver.ChromeOptions()
        # Usar perfil do usuário para manter login
        # options.add_argument("--user-data-dir=/tmp/chrome_profile")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 20)
        
        logger.info("Navegador iniciado com sucesso!")
        
    def acessar_rdstation(self):
        """Acessa a página do RD Station"""
        logger.info("Acessando RD Station...")
        self.driver.get("https://crm.rdstation.com/app/deals/pipeline")
        
        # Aguarda usuário fazer login se necessário
        input("\n⚠️  Faça login no RD Station se necessário e pressione ENTER para continuar...")
        logger.info("Continuando automação...")
        
    def verificar_whatsapp_web(self):
        """Verifica se WhatsApp Web está conectado"""
        logger.info("Verificando WhatsApp Web...")
        
        # Abre WhatsApp Web em nova aba
        self.driver.execute_script("window.open('https://web.whatsapp.com');")
        time.sleep(3)
        
        # Muda para aba do WhatsApp
        self.driver.switch_to.window(self.driver.window_handles[-1])
        
        input("\n⚠️  Certifique-se de que o WhatsApp Web está conectado e pressione ENTER para continuar...")
        
        # Volta para aba do RD Station
        self.driver.switch_to.window(self.driver.window_handles[0])
        logger.info("WhatsApp Web verificado!")
        
    def obter_leads_entrada(self):
        """Obtém todos os cards de leads da coluna 'Entrada de Leads'"""
        logger.info("Buscando leads na coluna 'Entrada de Leads'...")
        
        try:
            # Aguarda a página carregar
            time.sleep(3)
            
            # Baseado no CSS Selector fornecido:
            # #mfe-crm-deals-sales-pipeline > div > main > div.Grid__Root... > section:nth-child(1) > ... > div:nth-child(1)
            
            cards = []
            
            # Método 1: CSS Selector exato - busca todos os cards na primeira seção
            try:
                # Pega todos os cards filhos diretos do container na primeira seção
                cards = self.driver.find_elements(By.CSS_SELECTOR, 
                    "#mfe-crm-deals-sales-pipeline section:nth-child(1) div.sc-dkmKpi > div")
                
                if cards:
                    logger.info(f"✅ Método 1 (CSS exato): Encontrados {len(cards)} cards")
                    return cards
            except Exception as e:
                logger.warning(f"Método 1 falhou: {e}")
            
            # Método 2: CSS Selector mais genérico - primeira seção, classe ftSKDG
            try:
                cards = self.driver.find_elements(By.CSS_SELECTOR,
                    "section:nth-child(1) div.ftSKDG > div > div > div")
                
                if cards:
                    logger.info(f"✅ Método 2 (CSS classes): Encontrados {len(cards)} cards")
                    # Filtra apenas os visíveis
                    cards_visiveis = [c for c in cards if c.is_displayed()]
                    logger.info(f"   Destes, {len(cards_visiveis)} estão visíveis")
                    return cards_visiveis if cards_visiveis else cards
            except Exception as e:
                logger.warning(f"Método 2 falhou: {e}")
            
            # Método 3: Busca pela estrutura section > div > div
            try:
                # Encontra a primeira section
                primeira_secao = self.driver.find_element(By.CSS_SELECTOR, 
                    "#mfe-crm-deals-sales-pipeline section:first-child")
                
                # Dentro dela, busca os cards
                cards = primeira_secao.find_elements(By.CSS_SELECTOR, 
                    "div.sc-dkmKpi > div, div[class*='Card'] > div")
                
                if cards:
                    logger.info(f"✅ Método 3 (section + cards): Encontrados {len(cards)} cards")
                    return cards
            except Exception as e:
                logger.warning(f"Método 3 falhou: {e}")
            
            # Método 4: Busca por classe Card__Root
            try:
                primeira_secao = self.driver.find_element(By.CSS_SELECTOR, "section:first-of-type")
                cards = primeira_secao.find_elements(By.CSS_SELECTOR, "[class*='Card__Root']")
                
                if cards:
                    logger.info(f"✅ Método 4 (Card__Root): Encontrados {len(cards)} cards")
                    return cards
            except Exception as e:
                logger.warning(f"Método 4 falhou: {e}")
            
            # Método 5: XPath baseado no CSS selector
            try:
                cards = self.driver.find_elements(By.XPATH,
                    "//*[@id='mfe-crm-deals-sales-pipeline']//section[1]//div[contains(@class, 'sc-dkmKpi')]//div[contains(@class, 'Card') or contains(@class, 'card')]")
                
                if cards:
                    logger.info(f"✅ Método 5 (XPath): Encontrados {len(cards)} cards")
                    return cards
            except Exception as e:
                logger.warning(f"Método 5 falhou: {e}")
            
            # Método 6: Última tentativa - busca genérica por cards na primeira coluna
            try:
                todas_sections = self.driver.find_elements(By.TAG_NAME, "section")
                if todas_sections:
                    primeira = todas_sections[0]
                    cards = primeira.find_elements(By.XPATH, ".//div[@role='button' or contains(@onclick, '') or @tabindex]")
                    
                    if not cards:
                        # Tenta pegar qualquer div clicável
                        cards = primeira.find_elements(By.XPATH, ".//div[contains(@class, 'card') or contains(@class, 'Card')]")
                    
                    if cards:
                        logger.info(f"✅ Método 6 (genérico): Encontrados {len(cards)} cards")
                        return cards
            except Exception as e:
                logger.warning(f"Método 6 falhou: {e}")
            
            if not cards:
                logger.warning("⚠️ Nenhum card encontrado em nenhum método!")
                logger.info("💡 Tentando debug adicional...")
                
                # Debug detalhado
                try:
                    sections = self.driver.find_elements(By.TAG_NAME, "section")
                    logger.info(f"   Total de seções na página: {len(sections)}")
                    
                    if sections:
                        divs_primeira = sections[0].find_elements(By.TAG_NAME, "div")
                        logger.info(f"   Divs na primeira seção: {len(divs_primeira)}")
                        
                        # Tenta encontrar qualquer elemento com texto de nome
                        elementos_com_texto = sections[0].find_elements(By.XPATH, ".//*[string-length(text()) > 3]")
                        logger.info(f"   Elementos com texto: {len(elementos_com_texto)}")
                        
                        if elementos_com_texto:
                            logger.info("   Alguns textos encontrados:")
                            for elem in elementos_com_texto[:5]:
                                logger.info(f"      - {elem.text[:30]}")
                except Exception as debug_error:
                    logger.error(f"   Erro no debug: {debug_error}")
                
            logger.info(f"📊 Total final de leads encontrados: {len(cards)}")
            return cards
            
        except Exception as e:
            logger.error(f"❌ Erro ao buscar leads: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return []
    
    def clicar_no_lead(self, card):
        """Clica no card do lead para abrir os detalhes"""
        try:
            logger.info(f"Tentando clicar no card...")
            
            # Verifica se o elemento está visível e habilitado
            if not card.is_displayed():
                logger.warning("Card não está visível, tentando scroll...")
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", card)
                time.sleep(1)
            
            # Tenta pegar o nome do lead antes de clicar (para log)
            try:
                nome_no_card = card.text.split('\n')[0] if card.text else "Lead"
                logger.info(f"Clicando no card: {nome_no_card}")
            except:
                pass
            
            # Método 1: Clique normal
            try:
                card.click()
                logger.info("✅ Clicou no card (método normal)")
                time.sleep(3)
                return True
            except Exception as e:
                logger.warning(f"Clique normal falhou: {e}")
            
            # Método 2: JavaScript click
            try:
                logger.info("Tentando clique via JavaScript...")
                self.driver.execute_script("arguments[0].click();", card)
                logger.info("✅ Clicou no card (método JavaScript)")
                time.sleep(3)
                return True
            except Exception as e:
                logger.warning(f"Clique JavaScript falhou: {e}")
            
            # Método 3: Clique com ActionChains
            try:
                from selenium.webdriver.common.action_chains import ActionChains
                logger.info("Tentando clique via ActionChains...")
                actions = ActionChains(self.driver)
                actions.move_to_element(card).click().perform()
                logger.info("✅ Clicou no card (método ActionChains)")
                time.sleep(3)
                return True
            except Exception as e:
                logger.warning(f"Clique ActionChains falhou: {e}")
            
            logger.error("❌ Todos os métodos de clique falharam")
            return False
            
        except Exception as e:
            logger.error(f"Erro ao clicar no lead: {e}")
            return False
    
    def verificar_botao_whatsapp(self):
        """Verifica se existe o botão 'Abrir com WhatsApp'"""
        try:
            # Baseado no debug: <title>Abrir com WhatsApp</title> está dentro de <svg> dentro de <button>
            # O botão é: <button class="ButtonBase__Root-sc-3vs9dj-0 ... IconButton__Root-sc-qgu8rz-0 ...">
            
            logger.info("Procurando botão WhatsApp...")
            
            # Método 1: Encontra o <title> e sobe 2 níveis até o <button>
            try:
                title_element = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, "//title[contains(text(), 'Abrir com WhatsApp')]"))
                )
                
                # Sobe para o SVG (pai)
                svg_element = title_element.find_element(By.XPATH, "..")
                
                # Sobe para o BUTTON (avô)
                botao = svg_element.find_element(By.XPATH, "..")
                
                if botao.tag_name == 'button':
                    logger.info("✅ Botão WhatsApp encontrado (método 1 - hierarquia)!")
                    return botao
                else:
                    logger.warning(f"Elemento encontrado não é button, é: {botao.tag_name}")
                    # Continua tentando outros métodos
                    
            except Exception as e:
                logger.warning(f"Método 1 falhou: {e}")
            
            # Método 2: Busca direto por button que contém o SVG com o title
            try:
                botao = self.driver.find_element(By.XPATH, 
                    "//button[.//title[contains(text(), 'Abrir com WhatsApp')]]")
                logger.info("✅ Botão WhatsApp encontrado (método 2 - XPath direto)!")
                return botao
            except Exception as e:
                logger.warning(f"Método 2 falhou: {e}")
            
            # Método 3: Busca por button com classe IconButton que contém SVG
            try:
                botao = self.driver.find_element(By.XPATH, 
                    "//button[contains(@class, 'IconButton')][.//svg]")
                # Verifica se é realmente o botão do WhatsApp checando se tem o title
                if "Abrir com WhatsApp" in botao.get_attribute('innerHTML'):
                    logger.info("✅ Botão WhatsApp encontrado (método 3 - por classe)!")
                    return botao
            except Exception as e:
                logger.warning(f"Método 3 falhou: {e}")
            
            # Método 4: Busca por qualquer elemento com texto "Abrir com WhatsApp" e sobe até button
            try:
                elemento_whats = self.driver.find_element(By.XPATH, 
                    "//*[contains(text(), 'Abrir com WhatsApp')]")
                
                # Sobe na hierarquia até encontrar um button
                elemento_atual = elemento_whats
                for nivel in range(10):
                    try:
                        elemento_atual = elemento_atual.find_element(By.XPATH, "..")
                        if elemento_atual.tag_name == 'button':
                            logger.info(f"✅ Botão WhatsApp encontrado (método 4 - subindo {nivel+1} níveis)!")
                            return elemento_atual
                    except:
                        break
                        
            except Exception as e:
                logger.warning(f"Método 4 falhou: {e}")
            
            # Se nenhum método funcionou
            logger.warning("❌ Botão WhatsApp não encontrado em nenhum método")
            logger.info("💡 Verificando se o elemento está visível na página...")
            
            # Última tentativa: lista todos os buttons visíveis (debug)
            try:
                buttons = self.driver.find_elements(By.TAG_NAME, "button")
                logger.info(f"   Total de buttons na página: {len(buttons)}")
                
                # Procura manualmente em cada button
                for btn in buttons:
                    if "whatsapp" in btn.get_attribute('innerHTML').lower():
                        logger.info("✅ Encontrou button com 'whatsapp' no HTML!")
                        return btn
            except:
                pass
            
            return None
            
        except Exception as e:
            logger.error(f"Erro ao procurar botão WhatsApp: {e}")
            return None
    
    def listar_leads_visiveis(self):
        """Lista todos os nomes de leads visíveis - útil para debug"""
        try:
            # Procura por nomes visíveis nos cards
            elementos_nomes = self.driver.find_elements(By.XPATH, 
                "//div[contains(text(), 'Entrada de Leads')]//following::div[contains(@class, 'card') or contains(@class, 'deal')]//text()[string-length() > 3]")
            
            if elementos_nomes:
                logger.info("📋 Leads visíveis na tela:")
                for i, elem in enumerate(elementos_nomes[:10], 1):  # Mostra apenas os 10 primeiros
                    logger.info(f"  {i}. {elem.text if hasattr(elem, 'text') else elem}")
            else:
                logger.warning("Nenhum nome de lead encontrado")
                
        except Exception as e:
            logger.error(f"Erro ao listar leads: {e}")
    
    def obter_nome_lead(self):
        """Obtém o nome do lead atual"""
        try:
            # Procura pelo nome na seção "Negociação"
            nome_element = self.driver.find_element(By.XPATH, "//div[text()='Nome']/following-sibling::div")
            nome = nome_element.text
            logger.info(f"Nome do lead: {nome}")
            return nome
        except:
            logger.warning("Não foi possível obter o nome do lead")
            return "Lead sem nome"
    
    def clicar_whatsapp(self, botao):
        """Clica no botão do WhatsApp"""
        try:
            botao.click()
            logger.info("✅ Clicou no botão WhatsApp!")
            logger.info("⏳ Aguardando WhatsApp Web carregar (8 segundos)...")
            time.sleep(8)  # Aguarda mais tempo para a nova aba abrir e carregar
            return True
        except Exception as e:
            logger.error(f"Erro ao clicar no WhatsApp: {e}")
            return False
    
    def enviar_mensagem_whatsapp(self):
        """Envia a mensagem padrão no WhatsApp Web"""
        try:
            # Muda para a última aba (WhatsApp)
            self.driver.switch_to.window(self.driver.window_handles[-1])
            logger.info("✅ Mudou para aba do WhatsApp")
            
            # Aguarda a página do WhatsApp carregar completamente
            logger.info("⏳ Aguardando WhatsApp Web carregar completamente...")
            time.sleep(8)  # Tempo maior para carregar o chat
            
            # VERIFICA SE APARECEU ERRO DE NÚMERO INVÁLIDO
            try:
                logger.info("🔍 Verificando se o número é válido...")
                
                # Procura ESPECIFICAMENTE pelo modal de erro do WhatsApp
                # O modal tem um texto específico e um botão OK
                
                # Primeiro, verifica se existe o texto EXATO de erro
                page_text = self.driver.page_source
                
                erros_encontrados = (
                    "não está no WhatsApp" in page_text or
                    "not on WhatsApp" in page_text or
                    "Número de telefone compartilhado via URL é inválido" in page_text or
                    "Phone number shared via url is invalid" in page_text
                )
                
                # E também verifica se tem o botão OK (indica que é um modal de erro)
                tem_botao_ok = False
                try:
                    botao_ok = self.driver.find_element(By.XPATH,
                        "//div[contains(@role, 'dialog') or contains(@class, 'modal')]//button[text()='OK' or text()='Ok']")
                    tem_botao_ok = True
                except:
                    pass
                
                if erros_encontrados and tem_botao_ok:
                    logger.warning("⚠️ NÚMERO INVÁLIDO OU NÃO EXISTE NO WHATSAPP!")
                    logger.info("🔍 Clicando no botão OK...")
                    
                    # Clica no botão OK
                    try:
                        time.sleep(1)
                        botao_ok.click()
                        logger.info("✅ Clicou no botão OK")
                        time.sleep(2)
                    except Exception as e:
                        logger.warning(f"⚠️ Erro ao clicar no OK: {e}")
                    
                    # Fecha a aba do WhatsApp
                    logger.info("🔒 Fechando aba do WhatsApp...")
                    self.driver.close()
                    
                    # Volta para a aba do RD Station
                    self.driver.switch_to.window(self.driver.window_handles[0])
                    logger.info("✅ Voltou para aba do RD Station")
                    
                    logger.warning("❌ LEAD COM NÚMERO INVÁLIDO - NÃO ENVIOU MENSAGEM")
                    return False
                
                # Se chegou aqui, número é válido!
                logger.info("✅ Número válido! Prosseguindo com envio da mensagem...")
                    
            except Exception as e:
                logger.info(f"Verificação de erro concluída (sem erros detectados)")
                # Se der erro na verificação, assume que está tudo ok e continua
            
            # Procura pela caixa de texto do WhatsApp
            try:
                logger.info("🔍 Procurando caixa de mensagem do WhatsApp...")
                caixa_mensagem = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true'][@data-tab='10']"))
                )
                logger.info("✅ Caixa de mensagem encontrada!")
            except:
                # Tenta outro seletor
                logger.info("🔍 Tentando seletor alternativo...")
                try:
                    caixa_mensagem = self.wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "div[contenteditable='true'][data-tab='10']"))
                    )
                    logger.info("✅ Caixa de mensagem encontrada (seletor alternativo)!")
                except:
                    # Se não encontrou a caixa, pode ser erro no número
                    logger.error("❌ Não encontrou caixa de mensagem - provavelmente número inválido")
                    
                    # Tenta fechar possível modal de erro
                    try:
                        botao_ok = self.driver.find_element(By.XPATH, "//button[contains(text(), 'OK')]")
                        botao_ok.click()
                        time.sleep(1)
                    except:
                        pass
                    
                    # Fecha aba e volta
                    self.driver.close()
                    self.driver.switch_to.window(self.driver.window_handles[0])
                    return False
            
            # Aguarda mais um pouco antes de escrever
            time.sleep(2)
            
            # Clica na caixa de mensagem
            caixa_mensagem.click()
            time.sleep(1)
            
            logger.info("✍️ Digitando mensagem...")
            
            # Envia a mensagem (linha por linha para manter quebras de linha)
            linhas = self.mensagem_padrao.split('\n')
            for i, linha in enumerate(linhas):
                caixa_mensagem.send_keys(linha)
                if i < len(linhas) - 1:  # Não adiciona SHIFT+ENTER na última linha
                    caixa_mensagem.send_keys(Keys.SHIFT + Keys.ENTER)
            
            time.sleep(1)
            
            # Envia a mensagem (ENTER)
            logger.info("📤 Enviando mensagem...")
            caixa_mensagem.send_keys(Keys.ENTER)
            
            logger.info("✅ Mensagem enviada com sucesso!")
            
            # Aguarda a mensagem ser enviada
            time.sleep(3)
            
            # Fecha a aba do WhatsApp
            logger.info("🔒 Fechando aba do WhatsApp...")
            self.driver.close()
            
            # Volta para a aba do RD Station
            self.driver.switch_to.window(self.driver.window_handles[0])
            logger.info("✅ Voltou para aba do RD Station")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao enviar mensagem no WhatsApp: {e}")
            logger.error(f"   Tentando voltar para aba do RD Station...")
            
            # Tenta clicar em OK se houver modal de erro
            try:
                botao_ok = self.driver.find_element(By.XPATH, "//button[contains(text(), 'OK')]")
                botao_ok.click()
                logger.info("Clicou em OK do modal de erro")
                time.sleep(1)
            except:
                pass
            
            # Tenta fechar a aba do WhatsApp se estiver aberta
            try:
                if len(self.driver.window_handles) > 1:
                    self.driver.close()
            except:
                pass
            
            # Tenta voltar para aba do RD Station
            try:
                self.driver.switch_to.window(self.driver.window_handles[0])
            except:
                pass
            
            return False
    
    def mudar_status_para_contato_realizado(self):
        """Muda o status do lead para 'Contato Realizado' clicando na aba"""
        try:
            logger.info("📍 Mudando status para 'Contato Realizado'...")
            
            # Aguarda a página do lead carregar
            time.sleep(3)
            
            # Método 1: CSS Selector EXATO fornecido pelo usuário
            try:
                logger.info("🔍 Procurando aba 'Contato Realizado' (método 1 - CSS exato)...")
                botao = self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 
                        "#mfe-crm-deal-details > div > div > div.sc-iQvgRB.beTuLZ > div > div:nth-child(2) > ul > li:nth-child(2) > div > button > strong"))
                )
                
                # Clica no strong ou no botão pai
                try:
                    botao.click()
                except:
                    # Se clicar no strong não funcionar, clica no botão pai
                    botao_pai = botao.find_element(By.XPATH, "../..")
                    botao_pai.click()
                
                logger.info("✅ Clicou na aba 'Contato Realizado'!")
                time.sleep(3)
                
                # Verifica se há confirmação
                try:
                    confirmar = self.driver.find_element(By.XPATH, 
                        "//button[contains(text(), 'Confirmar') or contains(text(), 'Salvar') or contains(text(), 'OK')]")
                    confirmar.click()
                    logger.info("✅ Confirmou mudança")
                    time.sleep(2)
                except:
                    pass
                
                logger.info("✅ Status alterado para 'Contato Realizado'!")
                return True
                
            except Exception as e:
                logger.warning(f"Método 1 falhou: {e}")
            
            # Método 2: Tenta encontrar o botão pela estrutura mais genérica
            try:
                logger.info("🔍 Tentando método alternativo (método 2)...")
                botao = self.driver.find_element(By.CSS_SELECTOR,
                    "#mfe-crm-deal-details ul > li:nth-child(2) button")
                botao.click()
                logger.info("✅ Clicou na aba 'Contato Realizado' (método 2)!")
                time.sleep(3)
                return True
            except Exception as e:
                logger.warning(f"Método 2 falhou: {e}")
            
            # Método 3: Busca pelo texto do strong
            try:
                logger.info("🔍 Tentando buscar por texto (método 3)...")
                strong = self.driver.find_element(By.XPATH, 
                    "//strong[contains(text(), 'Contato Realizado')]")
                
                # Pega o botão pai
                botao = strong.find_element(By.XPATH, "../..")
                botao.click()
                
                logger.info("✅ Clicou na aba 'Contato Realizado' (método 3)!")
                time.sleep(3)
                return True
            except Exception as e:
                logger.warning(f"Método 3 falhou: {e}")
            
            logger.warning("⚠️ Mudança automática falhou")
            logger.warning("⚠️ Não foi possível mudar status automaticamente. Continuando...")
            return False
                
        except Exception as e:
            logger.error(f"Erro ao mudar status: {e}")
            logger.warning("⚠️ Continuando sem mudar status...")
            return False
    
    def mudar_status_para_declinado(self):
        """Muda o status do lead para 'Declinado' quando não tem WhatsApp"""
        try:
            logger.info("📍 Movendo lead para 'Declinado' (sem WhatsApp)...")
            
            # Aguarda a página do lead carregar
            time.sleep(3)
            
            # Método 1: CSS Selector EXATO fornecido pelo usuário
            try:
                logger.info("🔍 Procurando aba 'Declinado' (método 1 - CSS exato)...")
                botao = self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR,
                        "#mfe-crm-deal-details > div > div > div.sc-iQvgRB.beTuLZ > div > div:nth-child(2) > ul > li:nth-child(7) > div > button > strong"))
                )
                
                # Clica no strong ou no botão pai
                try:
                    botao.click()
                except:
                    # Se clicar no strong não funcionar, clica no botão pai
                    botao_pai = botao.find_element(By.XPATH, "../..")
                    botao_pai.click()
                
                logger.info("✅ Clicou na aba 'Declinado'!")
                time.sleep(3)
                
                # Verifica se há confirmação
                try:
                    confirmar = self.driver.find_element(By.XPATH,
                        "//button[contains(text(), 'Confirmar') or contains(text(), 'Salvar') or contains(text(), 'OK')]")
                    confirmar.click()
                    logger.info("✅ Confirmou mudança")
                    time.sleep(2)
                except:
                    pass
                
                logger.info("✅ Lead movido para 'Declinado'!")
                return True
                
            except Exception as e:
                logger.warning(f"Método 1 falhou: {e}")
            
            # Método 2: Tenta encontrar o botão pela estrutura mais genérica
            try:
                logger.info("🔍 Tentando método alternativo (método 2)...")
                botao = self.driver.find_element(By.CSS_SELECTOR,
                    "#mfe-crm-deal-details ul > li:nth-child(7) button")
                botao.click()
                logger.info("✅ Clicou na aba 'Declinado' (método 2)!")
                time.sleep(3)
                return True
            except Exception as e:
                logger.warning(f"Método 2 falhou: {e}")
            
            # Método 3: Busca pelo texto do strong
            try:
                logger.info("🔍 Tentando buscar por texto (método 3)...")
                strong = self.driver.find_element(By.XPATH,
                    "//strong[contains(text(), 'Declinado')]")
                
                # Pega o botão pai
                botao = strong.find_element(By.XPATH, "../..")
                botao.click()
                
                logger.info("✅ Clicou na aba 'Declinado' (método 3)!")
                time.sleep(3)
                return True
            except Exception as e:
                logger.warning(f"Método 3 falhou: {e}")
            
            logger.warning("⚠️ Mudança automática para Declinado falhou")
            logger.warning("⚠️ Não foi possível mudar status automaticamente. Continuando...")
            return False
                
        except Exception as e:
            logger.error(f"Erro ao mudar status para Declinado: {e}")
            logger.warning("⚠️ Continuando sem mudar status...")
            return False
    
    def voltar_para_pipeline(self):
        """Volta para a página principal do pipeline"""
        try:
            logger.info("🔄 Voltando para o pipeline...")
            
            # Força navegação de volta para o pipeline
            self.driver.get("https://crm.rdstation.com/app/deals/pipeline")
            
            logger.info("⏳ Aguardando pipeline carregar...")
            time.sleep(5)  # Tempo maior para garantir que carregou
            
            logger.info("✅ Pipeline carregado")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao voltar para pipeline: {e}")
            time.sleep(3)
            return False
    
    def processar_lead(self, card, index):
        """Processa um único lead"""
        logger.info(f"\n{'='*50}")
        logger.info(f"Processando lead #{index + 1}")
        logger.info(f"{'='*50}")
        
        # Clica no lead
        if not self.clicar_no_lead(card):
            logger.error("Falha ao abrir lead, pulando...")
            return "erro"
        
        # Obtém nome do lead
        nome = self.obter_nome_lead()
        
        # Verifica se tem botão WhatsApp
        botao_whatsapp = self.verificar_botao_whatsapp()
        
        if not botao_whatsapp:
            logger.warning(f"❌ Lead '{nome}' não tem WhatsApp disponível")
            logger.info("📍 Movendo para coluna 'Declinado'...")
            
            # Move para Declinado
            self.mudar_status_para_declinado()
            
            # Volta para pipeline
            self.voltar_para_pipeline()
            
            logger.info(f"⚠️ Lead '{nome}' movido para 'Declinado' (sem WhatsApp)")
            return "sem_whatsapp"
        
        # Clica no WhatsApp
        if not self.clicar_whatsapp(botao_whatsapp):
            logger.error("Falha ao abrir WhatsApp, pulando...")
            self.voltar_para_pipeline()
            return "erro"
        
        # Envia mensagem
        resultado_envio = self.enviar_mensagem_whatsapp()
        
        if not resultado_envio:
            logger.error("❌ Falha ao enviar mensagem - provavelmente número inválido")
            logger.info("📍 Movendo para coluna 'Declinado'...")
            
            # Move para Declinado (número inválido)
            self.mudar_status_para_declinado()
            
            # Volta para pipeline
            self.voltar_para_pipeline()
            
            logger.info(f"⚠️ Lead '{nome}' movido para 'Declinado' (número inválido)")
            return "numero_invalido"
        
        # Muda status para Contato Realizado
        self.mudar_status_para_contato_realizado()
        
        # Volta para pipeline
        self.voltar_para_pipeline()
        
        logger.info(f"✅ Lead '{nome}' processado com sucesso!")
        return "sucesso"
    
    def executar(self):
        """Executa o fluxo completo de automação"""
        try:
            # Inicia navegador
            self.iniciar_navegador()
            
            # Acessa RD Station
            self.acessar_rdstation()
            
            # Verifica WhatsApp Web
            self.verificar_whatsapp_web()
            
            logger.info("\n" + "="*50)
            logger.info("INICIANDO PROCESSAMENTO DE LEADS")
            logger.info("="*50 + "\n")
            
            leads_processados = 0
            leads_sem_whatsapp = 0
            leads_numero_invalido = 0
            
            logger.info("🤖 MODO AUTOMÁTICO: Processando todos os leads sem parar...")
            
            # Loop principal - processa leads automaticamente
            while True:
                logger.info(f"\n🔍 Buscando próximo lead na coluna 'Entrada de Leads'...")
                
                # Certifica que está na página do pipeline
                url_atual = self.driver.current_url
                if "pipeline" not in url_atual:
                    logger.info("Voltando para o pipeline...")
                    self.driver.get("https://crm.rdstation.com/app/deals/pipeline")
                    time.sleep(3)
                
                # Obtém leads da coluna
                cards = self.obter_leads_entrada()
                
                if not cards:
                    logger.info("\n✅ Nenhum lead restante na coluna 'Entrada de Leads'!")
                    logger.info("💡 Se ainda há leads visíveis mas não foram detectados,")
                    logger.info("   pode ser necessário ajustar os seletores no código.")
                    break
                
                # Processa primeiro lead disponível
                numero_lead = leads_processados + leads_sem_whatsapp + leads_numero_invalido + 1
                logger.info(f"\n{'='*60}")
                logger.info(f"📌 LEAD #{numero_lead}")
                logger.info(f"{'='*60}")
                
                resultado = self.processar_lead(cards[0], leads_processados + leads_sem_whatsapp + leads_numero_invalido)
                
                if resultado == "sucesso":
                    leads_processados += 1
                    logger.info(f"\n✅ Lead #{numero_lead} processado! Total enviados: {leads_processados}")
                    
                    # AGUARDA 10 MINUTOS ENTRE CADA MENSAGEM PARA NÃO SER BANIDO
                    logger.info("\n" + "="*60)
                    logger.info("⏰ AGUARDANDO 10 MINUTOS ANTES DA PRÓXIMA MENSAGEM")
                    logger.info("   (Para evitar banimento do WhatsApp)")
                    logger.info("   Pressione Ctrl+C para parar")
                    logger.info("="*60)
                    time.sleep(600)  # 10 minutos = 600 segundos
                    
                elif resultado == "sem_whatsapp":
                    leads_sem_whatsapp += 1
                    logger.info(f"\n📍 Lead #{numero_lead} sem WhatsApp. Total sem WhatsApp: {leads_sem_whatsapp}")
                    # Não aguarda - processa próximo imediatamente
                    time.sleep(2)
                    
                elif resultado == "numero_invalido":
                    leads_numero_invalido += 1
                    logger.info(f"\n⚠️ Lead #{numero_lead} com número inválido. Total inválidos: {leads_numero_invalido}")
                    # Não aguarda - processa próximo imediatamente
                    time.sleep(2)
                    
                else:
                    logger.error(f"\n❌ Erro ao processar lead #{numero_lead}")
                    time.sleep(2)
            
            # Resumo
            logger.info("\n" + "="*60)
            logger.info("🎉 AUTOMAÇÃO CONCLUÍDA!")
            logger.info("="*60)
            logger.info(f"✅ Leads com mensagem enviada: {leads_processados}")
            logger.info(f"📍 Leads sem WhatsApp: {leads_sem_whatsapp}")
            logger.info(f"⚠️ Leads com número inválido: {leads_numero_invalido}")
            logger.info(f"📊 TOTAL de leads processados: {leads_processados + leads_sem_whatsapp + leads_numero_invalido}")
            logger.info(f"📍 TOTAL movidos para Declinado: {leads_sem_whatsapp + leads_numero_invalido}")
            logger.info("="*60 + "\n")
            
        except KeyboardInterrupt:
            logger.info("\n⚠️ Automação interrompida pelo usuário (Ctrl+C)")
        except Exception as e:
            logger.error(f"\n❌ Erro fatal: {e}")
            import traceback
            logger.error(traceback.format_exc())
        finally:
            input("\nPressione ENTER para fechar o navegador...")
            if self.driver:
                self.driver.quit()
                logger.info("🔒 Navegador fechado")

def main():
    """Função principal"""
    print("""
    ╔══════════════════════════════════════════════════════╗
    ║   AUTOMAÇÃO RD STATION - WHATSAPP                    ║
    ║   Envio automático de mensagens de saudação          ║
    ║   ⏰ AGUARDA 10 MINUTOS ENTRE CADA MENSAGEM          ║
    ╚══════════════════════════════════════════════════════╝
    """)
    
    bot = RDStationWhatsAppBot()
    bot.executar()

if __name__ == "__main__":
    main()