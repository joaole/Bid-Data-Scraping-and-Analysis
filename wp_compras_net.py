from playwright.sync_api import sync_playwright
import time

def run(playwright):
    # Launch the browser
    browser = playwright.chromium.launch(headless=False)  # headless=False to see the browser actions
    page = browser.new_page()  # Open a new page

    # Navigate to the URL
    page.goto('https://comprasbr.com.br/pregao-eletronico/?objeto=M%C3%B3veis&utm_source=Google&utm_medium=Pesquisa&utm_campaign=AN009_pregao_de_moveis')

    #wait for the pages load
    time.sleep(5)

    # Scroll down to ensure all content is loaded
    print("Scrolling down to load all content...")
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(2)  # Wait a bit for any lazy-loaded content
    
    # Wait for the page to load and display the necessary elements
    print("Waiting for the page to load...")
    try:
        # Wait for the main container
        page.wait_for_selector('layout wrap align-center', timeout=30000)  # Increased timeout to 60 seconds
    except Exception as e:
        print(f"Error: {e}")
        browser.close()
        return


    # Extract the data
    print("Extracting data...")
    processos = []
    processo_cards = page.query_selector_all('.processo-card')
    for processo_card in processo_cards:
        numero_edital = processo_card.query_selector('.processo-card-capa-numero-edital').inner_text().strip()
        objeto = processo_card.query_selector('.processo-card-item-label-objeto').inner_text().strip()
        data_hora = processo_card.query_selector('.v-icon[aria-hidden="true"]:nth-child(1)').parent.inner_text().strip()
        local = processo_card.query_selector('.v-icon[aria-hidden="true"]:nth-child(2)').parent.inner_text().strip()
        tipo_licitacao = processo_card.query_selector('.v-icon[aria-hidden="true"]:nth-child(3)').parent.inner_text().strip()
        status = processo_card.query_selector('.processo-card-item-label-valor').inner_text().strip()
        
        processos.append([numero_edital, objeto, data_hora, local, tipo_licitacao, status])
    
    # Close the browser
    browser.close()

    # Print the extracted data
    for processo in processos:
        print(processo)

# Run the Playwright script
with sync_playwright() as playwright:
    run(playwright)
