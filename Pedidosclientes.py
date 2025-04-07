import streamlit as st

# Simulamos el catálogo de productos con modelos, marcas y colores
catalogo = {
    "Tenis": [
        {
            "marca": "Reebok",
            "colores": ["Rojo", "Azul", "Negro"],
            "tallas": [24, 25, 26, 27],
            "precio": 500
        },
        {
            "marca": "Nike",
            "colores": ["Blanco", "Negro", "Rojo"],
            "tallas": [24, 25, 26, 27],
            "precio": 600
        },
        {
            "marca": "Adidas",
            "colores": ["Negro", "Blanco", "Azul"],
            "tallas": [24, 25, 26, 27],
            "precio": 550
        }
    ],
    "Zapatos Escolares": [
        {
            "marca": "Nike",
            "colores": ["Blanco", "Negro"],
            "tallas": [22, 23, 24, 25],
            "precio": 420
        },
        {
            "marca": "Adidas",
            "colores": ["Negro", "Azul"],
            "tallas": [22, 23, 24, 25],
            "precio": 450
        }
    ],
    "Botines de Moda": [
        {
            "marca": "Puma",
            "colores": ["Negro", "Marrón", "Beige"],
            "tallas": [23, 24, 25, 26],
            "precio": 620
        },
        {
            "marca": "Reebok",
            "colores": ["Negro", "Blanco", "Gris"],
            "tallas": [23, 24, 25, 26],
            "precio": 650
        }
    ]
}

# Estilo para la página
st.set_page_config(page_title="Pedidos de Zapatos", layout="wide")

# Título de la página
st.title("🛍️ Sistema de Pedidos de Zapatos")
st.markdown("---")

# Menú lateral usando botones
st.sidebar.title("Menú de Navegación")
if st.sidebar.button("Catálogo"):
    seccion = "Catálogo"
elif st.sidebar.button("Carrito"):
    seccion = "Carrito"
else:
    seccion = "Catálogo"  # Predeterminado

# Inicializamos el carrito si no existe
if "carrito" not in st.session_state:
    st.session_state.carrito = []

# Sección del catálogo
if seccion == "Catálogo":
    st.header("📦 Catálogo de Productos")
    st.markdown("---")

    # Mostrar los modelos
    for modelo, productos in catalogo.items():
        # Usamos solo el título expandido con Markdown para tamaño más grande
        with st.expander(f"### **{modelo}**", expanded=False):  # Título más grande en negrita con Markdown
            for producto in productos:
                # Tarjeta para cada producto
                with st.container():
                    col1, col2 = st.columns([2, 1])  # Dividimos en 2 partes para descripción e imagen
                    
                    with col1:
                        st.subheader(f"**{producto['marca']} - {modelo}**")
                        st.write(f"💲 **Precio**: ${producto['precio']}")
                        st.write(f"📏 **Tallas disponibles**: {', '.join(map(str, producto['tallas']))}")
                        st.write(f"🎨 **Colores disponibles**: {', '.join(producto['colores'])}")

                    with col2:
                        st.image("https://via.placeholder.com/150", use_container_width=True)  # Imagen adaptable al ancho de la columna
                    
                    # Entradas de Talla, Color y Cantidad en una sola línea
                    col1, col2, col3, col4 = st.columns([2, 2, 2, 1])  # Dividimos en 4 partes
                    
                    # Selección de talla
                    talla = col1.selectbox("Talla", producto['tallas'], key=f"talla_{modelo}_{producto['marca']}")
                    
                    # Selección de color
                    color = col2.selectbox("Color", producto['colores'], key=f"color_{modelo}_{producto['marca']}")
                    
                    # Selección de cantidad (sin mostrar un valor por defecto de 0)
                    cantidad = col3.number_input("Cantidad", min_value=1, max_value=20, value=1, key=f"cantidad_{modelo}_{producto['marca']}")

                    # Aseguramos que la cantidad mínima sea 1, si es 0, la limpiamos
                    if cantidad == 0:
                        cantidad = 1
                    
                    # Botón de agregar al carrito con texto "Añadir al carrito"
                    if col4.button("🛒 Añadir al carrito", key=f"btn_{modelo}_{producto['marca']}"):
                        if talla and color:  # Verificamos que se haya seleccionado una talla y color válidos
                            if cantidad > 0:  # Solo agregamos si la cantidad es mayor a 0
                                item = {
                                    "modelo": modelo,
                                    "marca": producto['marca'],
                                    "talla": talla,
                                    "color": color,
                                    "cantidad": cantidad,
                                    "precio_unitario": producto['precio']
                                }
                                st.session_state.carrito.append(item)
                                st.success(f"✅ {producto['marca']} - {modelo} ({color}) añadido al carrito")
                            else:
                                st.warning("⚠️ La cantidad debe ser mayor que 0 para agregar al carrito.")
                        else:
                            st.warning("⚠️ Por favor selecciona una talla y un color antes de agregar al carrito.")

# Sección del carrito
elif seccion == "Carrito":
    st.header("🛒 Carrito de Compras")
    st.markdown("---")
    carrito = st.session_state.carrito

    if not carrito:
        st.info("Tu carrito está vacío. Agrega productos desde el catálogo.")
    else:
        total = 0
        for i, item in enumerate(carrito):
            cols = st.columns([3, 2, 2, 2, 1])
            cols[0].markdown(f"**{item['marca']} - {item['modelo']}**")
            cols[1].markdown(f"Talla: {item['talla']}")
            cols[2].markdown(f"Color: {item['color']}")
            cols[3].markdown(f"Cantidad: {item['cantidad']}")
            subtotal = item['cantidad'] * item['precio_unitario']
            cols[4].markdown(f"Subtotal: ${subtotal}")
            total += subtotal
            if cols[4].button("Eliminar", key=f"remove_{i}"):
                st.session_state.carrito.pop(i)
                st.experimental_rerun()

        st.markdown("---")
        st.subheader(f"**Total**: ${total}")

        nombre_cliente = st.text_input("🧾 Nombre o Código del Cliente")
        if st.button("Confirmar Pedido", key="confirmar"):
            if nombre_cliente:
                st.success("✅ Pedido confirmado. ¡Gracias por tu compra!")
                # Aquí podrías enviar a Google Sheets o a una base de datos
                st.session_state.carrito = []
            else:
                st.warning("⚠️ Por favor, ingresa tu nombre o código antes de confirmar.")
