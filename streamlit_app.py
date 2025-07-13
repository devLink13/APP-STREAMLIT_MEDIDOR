import streamlit as st

# verifica se a variável 'role' está presente nos estados da sessão.
# caso não esteja, define ela como None
if "role" not in st.session_state:
    st.session_state.role = None

# define uma lista de papéis possíveis para os usuários da sessão.
ROLES = [None, "Requester", "Responder", "Admin"]

# função de login, nesta funcao um cabeçalho de login é exibido e o usuário
# deve escolher seu papel, ao clicar no botão de login o papel selecionado 
# é armazenado no estado da sessão e a aplicação é recarregada
def login():

    st.header("Log in")
    role = st.selectbox("Selecione seu papel", ROLES)

    if st.button("Log in"):
        # adiciona o papel do usuário ao estado da sessão
        st.session_state.role = role
        # reinicia a sessão.
        st.rerun()

# esta função redefine o papel do usuário para None e recarrega a sessão.
def logout():
    st.session_state.role = None
    st.rerun()


role = st.session_state.role

# variáveis de página
logout_page = st.Page(logout, title="Log out", icon=":material/logout:")
settings = st.Page("settings.py", title="Settings", icon=":material/settings:")
request_1 = st.Page(
    "request/request_1.py",
    title="Request 1",
    icon=":material/help:",
    default=(role == "Requester"),
)
request_2 = st.Page(
    "request/request_2.py", title="Request 2", icon=":material/bug_report:"
)
respond_1 = st.Page(
    "respond/respond_1.py",
    title="Respond 1",
    icon=":material/healing:",
    default=(role == "Responder"),
)
respond_2 = st.Page(
    "respond/respond_2.py", title="Respond 2", icon=":material/handyman:"
)
admin_1 = st.Page(
    "admin/admin_1.py",
    title="Admin 1",
    icon=":material/person_add:",
    default=(role == "Admin"),
)
admin_2 = st.Page("admin/admin_2.py", title="Admin 2", icon=":material/security:")

# agrupamento de páginas por categoria
account_pages = [logout_page, settings]
request_pages = [request_1, request_2]
respond_pages = [respond_1, respond_2]
admin_pages = [admin_1, admin_2]


# define o titulo e o logo da aplicação
st.title("Request manager")
st.logo("images/horizontal_blue.png", icon_image="images/icon_blue.png")

# com base no papel do usuário deve ser criado um dicionário que contém 
# as páginas que cada um pode acessar

page_dict = {}
if st.session_state.role in ["Requester", "Admin"]:
    page_dict["Request"] = request_pages
if st.session_state.role in ["Responder", "Admin"]:
    page_dict["Respond"] = respond_pages
if st.session_state.role == "Admin":
    page_dict["Admin"] = admin_pages

# aplica a navegação de acordo com o papel selecionado
if len(page_dict) > 0:
    pg = st.navigation({"Account": account_pages} | page_dict)
else:
    pg = st.navigation([st.Page(login)])

pg.run()