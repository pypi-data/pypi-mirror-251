import gspread

credencial = r'.\cliente.json'
gc = gspread.service_account(credencial)


def Abrir_planilha(key = '1YAdc2ZefohO6o0532Tc34-huUIr5hUUS4WRXVmYDRZ8'):
    return gc.open_by_key(key)

def Criar_planilha(titulo):
    return gc.create(titulo)

def Selecionar_pagina(planilha, nome):
    return planilha.worksheet(nome)

def Criar_pagina(planilha, nome):
    return planilha.add_worksheet(title=nome, rows=100, cols=20)

def Deletar_pagina(planilha, pagina):
    planilha.del_worksheet(pagina)

def Ler_celulas(pagina, intervalo = "A1:B2"):
    return pagina.get(intervalo)

def Atualizar_celulas(pagina,intervaalo:str, valor:list[list] ):
    pagina.update(intervaalo, valor)



def Criar_pagina2(nome, key = '1YAdc2ZefohO6o0532Tc34-huUIr5hUUS4WRXVmYDRZ8', credencial = r'.\cliente.json'):
    return gspread.service_account(credencial).open_by_key(key).add_worksheet(title=nome, rows=100, cols=20)

def Ler_celulas2(intervalo = "A1:B2", key = '1YAdc2ZefohO6o0532Tc34-huUIr5hUUS4WRXVmYDRZ8', pagina = "campos do jordão", credencial = r'.\cliente.json'):
    return gspread.service_account(credencial).open_by_key(key).worksheet(pagina).get(intervalo)

def Atualizar_celulas2(valor:list[list],intervalo = "g1:h2", key = '1YAdc2ZefohO6o0532Tc34-huUIr5hUUS4WRXVmYDRZ8', pagina = "campos do jordão" , credencial = r'.\cliente.json'):
    gspread.service_account(credencial).open_by_key(key).worksheet(pagina).update(intervalo, valor)

# planilha = Abrir_planilha()
# pagina_campos_do_jordao = Selecionar_pagina(planilha, "campos do jordão")
