#SEMPRE COMEÇAR PELO PASSO A PASSO PARA SABER O QUE FAZER
#título - Sistema 
#Seção de cadastrar objetos
    #campo data
    #campo da pessoa - ana, bruno , carlos
    #campo do objeto - carro, avaliação , qualquer pesquisa de carater objeto ou conceito sentimento etc
    #campo da função por exemplo o que ele faz se o objeto tem uma quantidade se o objeto tem alguma função 
    #campo da variavel por exemplo variações do objeto por tipos como o valor varia de cada objeto ou o tipo é verde e anteriormente a função pode ser igual ou diferente
    #Botão para cadastrar seção dos sistema
        #atualizar a tabela da seção dos sistemas quando for clicado
#Seção de cadastrar as informações do sistema
    #tabela com os objetos
#Seção Dashboard
    #metrica/card ---> total de algum numero
    #Gráfico de Barra/Coluna -> pessoa por cadastro 
    #Gráfico de pizza --> objeto por cadastro
# streamlit o site que hospeda
# pandas a biblioteca que faz as tabelas base de dados
# plotly biblioteca para fazer gráficos
import streamlit as st
import pandas as pd
import plotly.express as px
from openai import OpenAI


#carregar tabela de dados
tabelaO = pd.read_csv("tabela(Planilha1).csv", sep = ";") #ele ta lendo a o arquivo do execell coloque um parametro que mostrar para sep coisas entre ;


st.set_page_config("Dosa",page_icon= "🐒")

st.write("# Sistema") #escreveu o titulo do site







#seção de cadastro 
#st.sidebar bota para ficar na barra lateral
st.sidebar.write("## Cadastrar objeto") # escreveu os topicos da tabela no menu do lado
data = st.sidebar.date_input("Data")
pessoa = st.sidebar.text_input("Quem tu é")
objeto = st.sidebar.text_input("O que é isso")
funcao = st.sidebar.text_input("O que isso faz")
variavel = st.sidebar.text_input("Existe oto que loco")
botao_cadastrar = st.sidebar.button("Termina o que tu quer bobão")

#logica de cadastro
if botao_cadastrar:
     nova_informacao = [str(data), pessoa, objeto, funcao, variavel]
     ultima_linha = len(tabelaO)
     tabelaO.loc[ultima_linha] = nova_informacao
     tabelaO.to_csv("tabela(Planilha1).csv", sep= ";", index= False)
     st.success("Conseguiu enviar bobao")
else:
     st.warning("Tem que resolver isso ai")





#seção de visualizar as variaveis
st.write("## Objetos variados") # escreveu os objetos da variavel  tabela
st.dataframe(tabelaO)

#seção de dashboard
st.write("## Dashboard") # total de alguma coisa e graficos

if not tabelaO.empty:
    moda = tabelaO["objeto"].mode()[0] # pega a moda do que aparece mais em objetos da parte da coluna objeto do parametro moda da parte [0] porque ai só aparece o primeiro que aparece e fica clean no codigo 
    st.metric("Objeto mais mais", value = moda)
    print(moda)
else:
     st.metric(" OBJETO MAIS MAIS:", value = "🙊Tem nada lol🙊")
 


#graficosssss1
grafico1 = px.bar(tabelaO, x= "pessoa", y= "objeto", color= "funcao")
st.plotly_chart(grafico1)
#grafosssss2
grafico2= px.pie(tabelaO, names= "funcao" , values= "variavel", hole= 0.5)
st.plotly_chart(grafico2)

# ia inteligente
modelo_ia = OpenAI(api_key = "" , base_url = 
"https://generativelanguage.googleapis.com/v1beta/openai" ) #biblioteca openia do gemini pq eu n to usando o proprio chat gpt
st.write("## ChatBot de Sasa") #quanto mais # menor fica o texto

#criar o historico de mensagems 
# 2. CRIAÇÃO DA MEMÓRIA DA TABELA: no mesmo formato de lista de mensagens
if "memoria_tabela" not in st.session_state:
    st.session_state["memoria_tabela"] = []
dados_atualizados_texto = tabelaO.to_string(index=False)
st.session_state["memoria_tabela"] = [
    {
        "role": "system", 
        "content": f"Dados atuais da tabela do sistema:\n\n{dados_atualizados_texto}"
    }
]



if not "lista_mensagens" in st.session_state:  #memoria da pagina
    st.session_state["lista_mensagens"] = []  # ele armazena no proprio session streaiamlit ou seja armazenei nele



mensagem_usuario = st.chat_input("Escreva a sua mensagem bobao") #o nome do que fica no box que escreve

for mensagem in st.session_state["lista_mensagens"]:

    quem_enviou = mensagem["role"]
    texto_mensagem = mensagem["content"]
    st.chat_message(quem_enviou).write(texto_mensagem)


if mensagem_usuario: 
    # se tiver uma mensagem vai exibir na tela
    #quem ta mandando a mensagem é o user -> usuario ou o assistant -> chatbot/robo/ia
    st.chat_message("user").write(mensagem_usuario) #chat message mostra e chat input pega uma informação
    mensagem = {"role": "user", "content": mensagem_usuario}
    st.session_state["lista_mensagens"].append(mensagem)
    pacote_completo_ia = st.session_state["memoria_tabela"] + st.session_state["lista_mensagens"]

    #pegar a resposta da ia 
    resposta_modelo = modelo_ia.chat.completions.create(messages = st.session_state["lista_mensagens"], model="gemini-flash-lite-latest") #modelo gemini gratuito
    resposta_ia = resposta_modelo.choices[0].message.content
    # e enviar a mensagem da Ia no chat

    with st.spinner("Consultando memórias..."):
        try:                            
            # Envia o pacote combinado para o modelo
            resposta_modelo = modelo_ia.chat.completions.create(
                messages=pacote_completo_ia, 
                model="gemini-flash-lite-latest"
            ) 
            
            # CORREÇÃO DA SINTAXE DA API: Acessando o conteúdo usando .choices[0] de forma correta
            resposta_ia = resposta_modelo.choices[0].message.content
            
            # Mostra e guarda a resposta da IA na lista de mensagens
            st.chat_message("assistant").write(resposta_ia)
            st.session_state["lista_mensagens"].append({"role": "assistant", "content": resposta_ia})
            
        except Exception as e:
            st.error(f"Erro na IA: {e}")

            #• with st.spinner("...")       O que faz: Cria a animação de "carregando" (bolinha girando) na tela.
	             #Para que serve: Avisa o usuário que o site está trabalhando e pensando, evitando que ele ache que a página travou.
            #• try (Tentar)
	            #O que faz: Envelopa o código que corre o risco de dar erro (como conexões de internet ou chamadas de IA).
               #Para que serve: Diz ao Python: "Tente rodar isso aqui. Se der certo, ótimo!"
            #• except (Exceção / Caso dê erro)
	            # O que faz: É o plano de emergência do try. Só roda se o código de cima falhar.
                #Para que serve: Evita que o seu site quebre e apareça aquela tela vermelha feia cheia de códigos. Em vez disso, ele captura o erro e mostra uma mensagem amigável que você escolher.
            # • completions.create(...)
	           #O que faz: Faz o envio oficial dos dados para o servidor da Inteligência Artificial.
              #Para que serve: Passa o histórico de mensagens, a tabela e escolhe qual modelo de IA (Gemini/GPT) vai processar a pergunta.
            #• .choices[0].message.content
	          #O que faz: Desembrulha o pacote gigante enviado pela IA e pega só o texto purinho da resposta. (Nota: no padrão correto da biblioteca, usa-se o índice da primeira opção: .choices[0]).
               #Para que serve: Isola a resposta do robô de dados técnicos inúteis para o usuário.
            #• st.chat_message("assistant").write(...)
              #O   que faz: Cria visualmente o balão de fala do robô no site.
              #•  Para que serve: Mostra a resposta da IA de forma organizada e bonita na tela do navegador.
             # st.session_state["..."].append(...)
	            # O que faz: Adiciona e "carimba" a última resposta do robô na memória temporária do site.
            	#Para que serve: Garante que o chat tenha memória e lembre do contexto na próxima pergunta que você fizer.
