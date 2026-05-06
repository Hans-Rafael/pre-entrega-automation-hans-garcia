import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.functions import inicializar_driver

class TestSauceDemo:

    def setup_method(self):
        """Este método se ejecuta antes de cada test"""
        self.driver = inicializar_driver()
        self.wait = WebDriverWait(self.driver, 10)

    def teardown_method(self):
        """Este método se ejecuta al finalizar cada test"""
        self.driver.quit()

    def test_login_exitoso(self):
        """Test que verifica login exitoso en SauceDemo"""
        # 1. Navegar
        self.driver.get('https://saucedemo.com')
        
        # 2. Ingresar credenciales (Esperas explícitas)
        user_input = self.wait.until(EC.presence_of_element_located((By.ID, 'user-name')))
        user_input.send_keys('standard_user')
        
        self.driver.find_element(By.ID, 'password').send_keys('secret_sauce')
        self.driver.find_element(By.ID, 'login-button').click()

        # 3. Validaciones obligatorias
        assert '/inventory.html' in self.driver.current_url
        
        header_title = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'title')))
        assert header_title.text == 'Products'
        
        print("\nTest Login: OK")

    def test_verificar_catalogo(self):
        """Test que verifica funcionamiento del catálogo de productos"""
        # Reutilizamos el login rápido para probar el catálogo
        self.test_login_exitoso() 
        
        # 1. Validar presencia de productos
        productos = self.driver.find_elements(By.CLASS_NAME, 'inventory_item')
        assert len(productos) > 0
        
        # 2. Listar nombre y precio del primero (Criterio mínimo)
        nombre = productos[0].find_element(By.CLASS_NAME, 'inventory_item_name').text
        precio = productos[0].find_element(By.CLASS_NAME, 'inventory_item_price').text
        
        # Primero validamos...
        assert nombre != "", "El nombre del producto no debería estar vacío"
        assert precio != "", "El precio del producto no debería estar vacío"
        
        # ...y si pasa, imprimimos
        print(f"\nProducto destacado: {nombre} a {precio}")
        
    def test_agregar_al_carrito(self):
        """Test que verifica agregar un producto al carrito"""
        # 1. Login previo
        self.test_login_exitoso()
        # 2. Agregar primer producto
        btn_agregar = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn_inventory')))
        btn_agregar.click()
        # con un css selector
        ##btn_agregar = self.driver.find_element(By.CSS_SELECTOR, ".inventory_item:nth-child(1) button")
        ##btn_agregar.click()
         
        # 3. Verificar que el contador (badge) del carrito aumentó a 1 (espera explícita)
        badge = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'shopping_cart_badge')))
        assert badge.text == '1'
        
        # 4. Ir al carrito y verificar producto
        self.driver.find_element(By.CLASS_NAME, 'shopping_cart_link').click()
        assert '/cart.html' in self.driver.current_url
        
        item_en_carrito = self.driver.find_element(By.CLASS_NAME, 'inventory_item_name')
        assert item_en_carrito.is_displayed()
        assert item_en_carrito.text != "" #agregada por buenas practica a pesar no necesitar esta la linea
        print(f"\nCarrito OK: Producto '{item_en_carrito.text}' verificado.")
        
