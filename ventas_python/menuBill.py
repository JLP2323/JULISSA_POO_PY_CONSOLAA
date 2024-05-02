import datetime
import json
import os
import time
import msvcrt  
import datetime
from abc import ABC
from colorama import init, Fore, Style
from functools import reduce
from company import Company
from components import Menu, Valida
from customer import RegularClient, JsonFile
from iCrud import ICrud
from product import Product
from sales import Sale
from utilities import borrarPantalla, gotoxy
from utilities import reset_color, red_color, green_color, blue_color, purple_color

path, _ = os.path.split(os.path.abspath(__file__))


def saveClient(dni, first_name, last_name, valor, json_file):
  client = {
    "dni": dni,
    "first_name": first_name,
    "last_name": last_name,
    "valor": valor
  }

  old_data = json_file.read()
  if old_data is not None:
    old_clients = json.loads(old_data)
  else:
    old_clients = []

  old_clients.append(client)

  json_file.write(json.dumps(old_clients))
  
def saveProduct(id, descripcion, precio, stock, json_file):
  product = {
    "id": id,
    "descripcion": descripcion,
    "precio": precio,
    "stock": stock
  }

  old_data_products = json_file.read()
  if old_data_products is not None:
    old_products = json.loads(old_data_products)
  else:
    old_products = []

  old_products.append(product)

  json_file.write(json.dumps(old_products))

class CrudClients(ICrud, ABC):
  def create(self):
    json_file_path = path + '/archivos/clients.json'
    json_file = JsonFile(json_file_path)

    while True:
        borrarPantalla()
        print('Registrando cliente.')
        dni = input("Ingresar cédula: ").strip()
        if ' ' in dni:
            print("Cedula invalida")
            time.sleep(2)
            continue
        if not dni.isdigit():
            print("Cedula invalida")
            time.sleep(2)
            continue
        if len(dni) != 10:
            print("Cedula invalida")
            time.sleep(2)
            continue

        first_name = input("Ingresar nombres completos: ").strip()
        if not all(c.isalpha() or c.isspace() for c in first_name):
            print("Nombres mal tipados")
            time.sleep(2)
            continue
        if len(first_name.split()) != 2:
            print("Nombres mal tipados")
            time.sleep(2)
            continue

        last_name = input("Ingresar apellidos completos: ").strip()
        if not all(c.isalpha() or c.isspace() for c in last_name):
            print("Apellidos mal tipado.")
            time.sleep(2)
            continue
        if len(last_name.split()) != 2:
            print("Apellidos mal tipado.")
            time.sleep(2)
            continue

        cliente = input("Usted es cliente regular o VIP? : ").lower()

        if cliente == "regular":
            valor = 0.10
            valor = round(valor, 2)  
        elif cliente == "vip":
            limite_vip = float(input("Ingresar el límite VIP del cliente : "))
            if limite_vip > 20000:
                limite_vip = 10000
            elif limite_vip < 10000:
                limite_vip = 10000
            else:
                limite_vip = round(limite_vip, 2)  
            valor = limite_vip

        borrarPantalla()
        print("Datos")
        smsCliente = input("regular o VIP?: ").lower()
        if smsCliente == "regular":
            print(
            f" DNI : {dni} \n Nombres : {first_name}\n Apellidos : {last_name}\n Descuento por ser regular cliente : {valor}")
            if input(" Guardar yes o no ? (YES/NO) : ").lower() == 'yes':
                saveClient(dni, first_name, last_name, valor, json_file)
                print("Cliente se guardó.")
                time.sleep(2)
            else:
                print("Cliente no se guardó.")
                time.sleep(2)
            break
        elif cliente == "vip":
            print(
            f"DNI : {dni} \n Nombres : {first_name}\n Apellidos : {last_name}\n Límite de crédito : {valor}")
            if input("Guardar yes o no ? (YES/NO) : ").lower() == 'yes':
                saveClient(dni, first_name, last_name, valor, json_file)
                print("Cliente se guardó.")
                time.sleep(2)
            else:
                print("Cliente no se guardó.")
                time.sleep(2)
            break

  def update(self):
    json_file_path = path + '/archivos/clients.json'
    json_file = JsonFile(json_file_path)

    while True:
        borrarPantalla()
        print('Actualizar cliente.')
        print()
        dni = input("Ingresar cédula, para actualizar datos del cliente : ").strip()
        if ' ' in dni:
            print("Cédila invalida")
            time.sleep(2)
            continue
        if not dni.isdigit():
            print("Cédila invalida")
            time.sleep(2)
            continue
        if len(dni) != 10:
            print("Cédila invalida")
            time.sleep(2)
            continue

        old_clients = json.loads(json_file.read() or '[]')

        for client in old_clients:
            if client["dni"] == dni:
                while True:
                    borrarPantalla()
                    print('Actualizando cliente.')
                    print()
                    dni = input("Ingresar número de cédula : ").strip()
                    if ' ' in dni:
                        print("Cédula invalidad.")
                        time.sleep(1)
                        continue
                    if not dni.isdigit():
                        print("Cédula invalidad.")
                        time.sleep(1)
                        continue
                    if len(dni) != 10:
                        print("Cédula invalidad.")
                        time.sleep(1)
                        continue

                    first_name = input("Ingresar nombres : ").strip()
                    if not all(c.isalpha() or c.isspace() for c in first_name):
                        print("Nombres mal tipado.")
                        time.sleep(1)
                        continue
                    if len(first_name.split()) != 2:
                        print("Nombres mal tipado.")
                        time.sleep(1)
                        continue
                    if any(len(name) < 3 for name in first_name.split()):
                        print("Nombres mal tipado.")
                        time.sleep(1)
                        continue

                    last_name = input("Ingresar apellidos : ").strip()
                    if not all(c.isalpha() or c.isspace() for c in last_name):
                        print("Apellidos mal tipado.")
                        time.sleep(1)
                        continue
                    if len(last_name.split()) != 2:
                        print("Apellidos mal tipado.")
                        time.sleep(1)
                        continue
                    if any(len(lastname) < 3 for lastname in last_name.split()):
                        print("Apellidos mal tipado.")
                        time.sleep(1)
                        continue

                    cliente = input("Usted es cliente regular o VIP? (regular/vip) : ").lower()

                    if cliente == "regular":
                        valor = 0.10
                        valor = round(valor, 2)  
                    elif cliente == "vip":
                        limite_vip = float(input("Ingresar el límite VIP del cliente : "))
                        if limite_vip > 20000:
                            limite_vip = 10000
                        elif limite_vip < 10000:
                            limite_vip = 10000
                        else:
                            limite_vip = round(limite_vip, 2)  
                        valor = limite_vip

                    borrarPantalla()
                    print("\n Datos")
                    if cliente == "regular":
                        print(
                            f" DNI : {dni} \n Nombres : {first_name}\n Apellidos : {last_name}\n Descuento por ser cliente regular : {valor}")
                    elif cliente == "vip":
                        print(
                            f"DNI : {dni} \nNombres : {first_name}\nApellidos : {last_name}\nLímite de crédito VIP : {valor}")

                    if input("Guardar yes o no ? (YES/NO) : ").lower() == 'yes':
                        client["dni"] = dni
                        client["first_name"] = first_name
                        client["last_name"] = last_name
                        client["valor"] = float(valor)
                        json_file.write(json.dumps(old_clients))
                        print("Cliente actualizado.")
                        time.sleep(2)
                        break
                    else:
                        print("Cancelada.")
                        time.sleep(2)
                        break

        else:
            print("Cliente no encontrado")
            
        break

  def delete(self):
    json_file_path = path + '/archivos/clients.json'
    json_file = JsonFile(json_file_path)

    while True:
        borrarPantalla()
        print('Eliminará datos del cliente.')
        print()
        dni = input("Ingresar cédula : ").strip()
        if ' ' in dni:
            print("Cédula invalidad.")
            time.sleep(1)
            continue
        if not dni.isdigit():
            print("Cédula invalidad.")
            time.sleep(1)
            continue
        if len(dni) != 10:
            print("Cédula invalidad.")
            time.sleep(1)
            continue

        old_clients = json.loads(json_file.read() or "[]")

        updated_clients = [client for client in old_clients if client["dni"] != dni]
        deleted = len(updated_clients) != len(old_clients)

        if deleted:
            borrarPantalla()
            print("Verificar Datos")
            print()
            client_to_delete = next((client for client in old_clients if client["dni"] == dni), None)
            print("DNI:", dni)
            print("Nombres:", client_to_delete["first_name"])
            print("Apellidos:", client_to_delete["last_name"])
            print("Crédito:", client_to_delete["valor"])
            aceptar = input("Eliminar cliente. ? (YES/NO) ").lower()

            if aceptar == 'yes':
                print("Cliente eliminados.")
                json_file.write(json.dumps(updated_clients))
                time.sleep(2)
            else:
                print("Cancelada")
                time.sleep(2)
        else:
            print("\nCliente no existe.")
            time.sleep(2)
            continue

        break

  def consult(self):
    json_file_path = path + '/archivos/clients.json'
    json_file = JsonFile(json_file_path)

    while True:
        borrarPantalla()
        print('Consultar cliente.')
        print()
        dni = input("Ingresar cédula : ").strip()
        if ' ' in dni:
            print("Cédula invalidad.")
            time.sleep(1)
            continue
        if not dni.isdigit():
            print("Cédula invalidad.")
            time.sleep(1)
            continue
        if len(dni) != 10:
            print("Cédula invalidad.")
            time.sleep(1)
            continue

        old_clients = json.loads(json_file.read() or "[]")

        if not old_clients:
            print("Datos del json vacío")
            return

        found_clients = [client for client in old_clients if client["dni"] == dni]
        if found_clients:
            borrarPantalla()
            print("\nConsultando cliente")
            print("\n" + "DNI".ljust(30) + "Nombres".ljust(30) + "Apellido".ljust(30) + "LÍMITE DEL CRÉDITO")
            for client in found_clients:
                print(str(client["dni"]).ljust(30), (client["first_name"]).ljust(30),
                      client["last_name"].ljust(30), client["valor"])
                time.sleep(5)
                input("-")
        else:
            print("Cliente no existe.")
            time.sleep(2)
            continue
            
        break


class CrudProducts(ICrud):
  def create(self):
    json_file_path = path + '/archivos/products.json'
    json_file = JsonFile(json_file_path)

    while True:
        borrarPantalla()
        print('Registrando datos del producto.')
        print()
        id = input("Ingresar id del producto : ").strip()
        if ' ' in id:
            print("Id invalido.")
            time.sleep(2)
            continue
        if not id.isdigit():
            print("Id invalido.")
            time.sleep(2)
            continue
        if len(id) != 1:
            print("Id invalido.")
            time.sleep(2)
            continue

        descripcion = input("Ingresar descripción del producto : ").strip()
        if not all(c.isalpha() or c.isspace() for c in descripcion):
            print("Ponga descripción correcta.")
            time.sleep(2)
            continue
        if any(len(descrip) < 3 for descrip in descripcion.split()):
            print("Ponga descripción correcta.")
            time.sleep(2)
            continue

        precio = input("Ingresar precio del producto : ").strip()
        if not precio.replace('.', '', 1).replace('-', '', 1).isdigit():
            print("Solo datos numericos.")
            time.sleep(2)
            continue
        if float(precio) < 0:
            print("Solo datos numericos.")
            time.sleep(2)
            continue

        stock = input("Ingresar el stock del producto : ").strip()
        if not stock.replace('.', '', 1).replace('-', '', 1).isdigit():
            print("Solo datos numericos.")
            time.sleep(2)
            continue
        if float(stock) < 0:
            print("Solo datos numericos.")
            time.sleep(2)
            continue
          
        precio = float(precio)
        stock = int(stock)

        borrarPantalla()
        print("\n Verificar Datos")
        print()
        print(f" ID: {id}\n Descripción: {descripcion}\n Precio $: {precio}\n Stock: {stock}")
        if input("Guardar producto ? (YES/NO) ").lower() == 'yes':
            saveProduct(id, descripcion, precio, stock, json_file)
            print("Producto guardadp.")
            time.sleep(2)
        else:
            print("No guardado.")
            time.sleep(2)

        break

  def update(self):
    json_file_path = path + '/archivos/products.json'
    json_file = JsonFile(json_file_path)

    while True:
        borrarPantalla()
        print('Actualizar producto.')
        print()
        id = input("Ingresar id del producto : ").strip()
        if ' ' in id:
            print("Id invalido.")
            time.sleep(2)
            continue
        if not id.isdigit():
            print("Id invalido.")
            time.sleep(2)
            continue
        if len(id) != 1:
            print("Id invalido.")
            time.sleep(2)
            continue
          
        old_products = json.loads(json_file.read() or '[]')
        
        for product in old_products:
          if product["id"] == id:
             while True:
              borrarPantalla()
              print('Actualizando datos del producto.')
              id = input("Ingresar id del producto : ").strip()
              if ' ' in id:
                  print("Id invalido.")
                  time.sleep(2)
                  continue
              if not id.isdigit():
                  print("Id invalido.")
                  time.sleep(2)
                  continue
              if len(id) != 1:
                  print("Id invalido.")
                  time.sleep(2)
                  continue
              
              descripcion = input("Ingresar descripción del producto : ").strip()
              if not all(c.isalpha() or c.isspace() for c in descripcion):
                  print("Ponga descripción correcta.")
                  time.sleep(2)
                  continue
              if any(len(descrip) < 3 for descrip in descripcion.split()):
                  print("Ponga descripción correcta.")
                  time.sleep(2)
                  continue
              
              precio = input("Ingresar precio del producto : ").strip()
              if not precio.replace('.', '', 1).replace('-', '', 1).isdigit():
                  print("Solo datos numericos.")
                  time.sleep(2)
                  continue
              if float(precio) < 0:
                  print("Solo datos numericos.")
                  time.sleep(2)
                  continue
              
              stock = input("Ingresar el stock del producto : ").strip()
              if not stock.replace('.', '', 1).replace('-', '', 1).isdigit():
                  print("Solo datos numericos.")
                  time.sleep(2)
                  continue
              if float(stock) < 0:
                  print("Solo datos numericos.")
                  time.sleep(2)
                  continue
              
              precio = float(precio)
              stock = int(stock)
                      
              borrarPantalla()
              print("\nVerificar Datos")
              print(f" ID : {id}\n Descripción : {descripcion}\n Precio $ : {precio}\n Stock : {stock}")
              aceptar = input("¿Aceptar y guardar? (YES/NO) => ").lower()
              
              if aceptar == 'yes':
                  product["id"] = id
                  product["descripcion"] = descripcion
                  product["precio"] = precio
                  product["stock"] = stock
                  json_file.write(json.dumps(old_products))
                  print("Producto actualizado.")
                  time.sleep(2)
                  return
              else:
                  print("Cancelado.")
                  time.sleep(2)
                
              break
                    
        print("Producto no encontrado.")

  def delete(self):
    json_file_path = path + '/archivos/products.json'
    json_file = JsonFile(json_file_path)

    while True:
        borrarPantalla()
        print('Eliminará producto.')
        print()
        id = input("Ingresar id del producto : ").strip()
        if ' ' in id:
            print("Id invalido.")
            time.sleep(2)
            continue
        if not id.isdigit():
            print("Id invalido.")
            time.sleep(2)
            continue
        if len(id) != 1:
            print("Id invalido.")
            time.sleep(2)
            continue
          
        old_products = json.loads(json_file.read() or '[]')
        
        updated_products = [product for product in old_products if product["id"] != id]
        deleted = len(updated_products) != len(old_products)
        
        if deleted:
            borrarPantalla()
            print("\n Verificar Datos")
            product_to_delete = next((product for product in old_products if product["id"] == id), None)
            print(" ID :", id)
            print(" Descripción :", product_to_delete["descripcion"])
            print(" Precio :", product_to_delete["precio"])
            print(" Stock :", product_to_delete["stock"])
            aceptar = input("Eliminar producto. ? (YES/NO) : ").lower()

            if aceptar == 'yes':
                print("producto eliminado.")
                json_file.write(json.dumps(updated_products))
                time.sleep(2)
            else:
                print("Cancelada.")
                time.sleep(2)
              
        else:
            print("Producto no encontrado.")
        
        break

  def consult(self):
    json_file_path = path + '/archivos/products.json'
    json_file = JsonFile(json_file_path)

    while True:
        borrarPantalla()
        print('Consultar producto.')
        print()
        id = input("Ingresar id del producto : ").strip()
        if ' ' in id:
            print("Id invalido.")
            time.sleep(2)
            continue
        if not id.isdigit():
            print("Id invalido.")
            time.sleep(2)
            continue
        if len(id) != 1:
            print("Id invalido.")
            time.sleep(2)
            continue
          
        old_products = json.loads(json_file.read() or '[]')
        
        if not old_products:
            print("Json sin datos")
            return
      
        found_product = [product for product in old_products if product["id"] == id]
        if found_product:
            borrarPantalla()
            print("\n Consultando Datos")
            print("ID".ljust(30) + "Descripción".ljust(30) + "Precio".ljust(30) + "Stock")
            for product in found_product:
                id_str = str(product["id"]).ljust(30)
                descripcion_str = str(product["descripcion"]).ljust(30)
                precio_str = str(product["precio"]).ljust(30)
                stock_str = str(product["stock"])
                print(id_str, descripcion_str, precio_str, stock_str)
                time.sleep(5)
                input("\nPresione tecla para continuar...")
        else:
            print("No existe producto.")
            time.sleep(2)
            continue
            
        break

class CrudSales(ICrud):
  def create(self):
    validar = Valida()
    borrarPantalla()
    print('\033c', end='')
    gotoxy(2,1);print(green_color+"██"*50+reset_color)
    gotoxy(30,2);print(blue_color+"Registro de Venta")
    gotoxy(17,3);print(blue_color+Company.get_business_name())
    gotoxy(5,4);print(f"Factura#:F0999999 {' '*3} Fecha:{datetime.datetime.now()}")
    gotoxy(66,4);print(" Subtotal:")
    gotoxy(66,5);print(" Decuento:")
    gotoxy(66,6);print(" Iva     :")
    gotoxy(66,7);print(" Total   :")
    gotoxy(10,6);print("Cedula:")
    dni = validar.solo_numeros("Error: Solo numeros",23,6)
    
    json_file = JsonFile(path+'/archivos/clients.json')
    clients_data = json_file.find("dni", dni)
    if not clients_data:
        gotoxy(35,6);print("Cliente no existe")
        return
    client = clients_data[0]
    cli = RegularClient(client["first_name"], client["last_name"], client["dni"], card=True) 
    sale = Sale(cli)
    gotoxy(35,6);print(cli.fullName())
    gotoxy(2,8);print(green_color+"██"*50+reset_color) 
    gotoxy(5,9);print(purple_color+"Linea") 
    gotoxy(12,9);print("Id_Articulo") 
    gotoxy(24,9);print("Descripcion") 
    gotoxy(38,9);print("Precio") 
    gotoxy(48,9);print("Cantidad") 
    gotoxy(58,9);print("Subtotal") 
    gotoxy(70,9);print("n->Terminar Venta)"+reset_color)
    
    follow = "s"
    line = 1
    while follow.lower() == "s":
        gotoxy(7,9+line);print(line)
        gotoxy(15,9+line);id_articulo = validar.solo_numeros("Error: Solo numeros",15,9+line)
        
        json_file = JsonFile(path+'/archivos/products.json')
        prods = json_file.find("id", id_articulo)
        if not prods:
            gotoxy(24,9+line);print("Producto no existe")
            time.sleep(1)
            gotoxy(24,9+line);print(" "*20)
        else:    
            prods = prods[0]
            product = Product(prods["id"], prods["descripcion"], prods["precio"], prods["stock"])
            gotoxy(24,9+line);print(product.descrip)
            gotoxy(38,9+line);print(product.preci)
            gotoxy(49,9+line);qty = int(validar.solo_numeros("Error: Solo numeros",49,9+line))
            gotoxy(59,9+line);print(product.preci * qty)
            sale.add_detail(product, qty)
            gotoxy(76,4);print(round(sale.subtotal,2))
            gotoxy(76,5);print(round(sale.discount,2))
            gotoxy(76,6);print(round(sale.iva,2))
            gotoxy(76,7);print(round(sale.total,2))
            gotoxy(74,9+line);follow = input() or "s"  
            gotoxy(76,9+line);print(green_color+"✔"+reset_color)  
            line += 1
    
    gotoxy(15,9+line);print(red_color+"Esta seguro de grabar la venta(s/n):")
    gotoxy(54,9+line);procesar = input().lower()
    if procesar == "s":
        gotoxy(15,10+line);print("😊 Venta Grabada satisfactoriamente 😊"+reset_color)
        json_file = JsonFile(path+'/archivos/invoices.json')
        invoices = json_file.read()
        if invoices:
            invoices = json.loads(invoices) 
            ult_invoices = invoices[-1]["factura"] + 1
        else:
            ult_invoices = 1

        json_file = JsonFile(path+'/archivos/invoices.json')
        data = sale.getJson()
        data["factura"] = ult_invoices
        json_file.append(data)

    else:
        gotoxy(20,10+line);print("🤣 Venta Cancelada 🤣"+reset_color)    
    time.sleep(2)

  def update(self):
    while True:
        borrarPantalla()
        print('Actualizar datos de la factura.')
        print()
        fact = input("Ingresar número de factura, para actualizar los datos :").strip()
        if ' ' in fact or not fact.isdigit() or len(fact) != 1:
            print("Numero de factura incorrecto.")
            time.sleep(2)
            continue
    
        fact = float(fact)
        json_file = JsonFile(path+'/archivos/invoices.json')
        clients_data = json_file.find("factura", fact)

        if clients_data:
            factura_encontrada = clients_data[0]  
            
            print("Cliente  : ", factura_encontrada["cliente"])
            print(f"Factura#: {factura_encontrada['factura']} {' '*3} Fecha:{factura_encontrada['Fecha']}")
            print("Subtotal : ", factura_encontrada["subtotal"])
            print("Descuento: ", factura_encontrada["descuento"])
            print("IVA      : ", factura_encontrada["iva"])
            print("Total    : ", factura_encontrada["total"])
          
            print()            
            input("Enter seguir datos a actualizar ")

            validar = Valida()
            borrarPantalla()
            print('\033c', end='')
            gotoxy(2,1);print(green_color+"██"*50+reset_color)
            gotoxy(30,2);print(blue_color+"Registro de Venta")
            gotoxy(17,3);print(blue_color+Company.get_business_name())
            gotoxy(5,4);print(f"Factura#: {factura_encontrada['factura']} {' '*3} Fecha:{datetime.datetime.now()}")
            gotoxy(66,4);print(" Subtotal:")
            gotoxy(66,5);print(" Descuento:")
            gotoxy(66,6);print(" IVA     :")
            gotoxy(66,7);print(" Total   :")
            gotoxy(10,6);print("Cedula:")
            dni = validar.solo_numeros("Error: Solo numeros",23,6)

            json_file = JsonFile(path+'/archivos/clients.json')
            clients_data = json_file.find("dni", dni)
            if not clients_data:
                gotoxy(35,6);print("Cliente no existe")
                return
            client = clients_data[0]
            cli = RegularClient(client["first_name"], client["last_name"], client["dni"], card=True) 
            sale = Sale(cli)
            gotoxy(35,6);print(cli.fullName())
            gotoxy(2,8);print(green_color+"██"*50+reset_color) 
            gotoxy(5,9);print(purple_color+"Linea") 
            gotoxy(12,9);print("Id_Articulo") 
            gotoxy(24,9);print("Descripcion") 
            gotoxy(38,9);print("Precio") 
            gotoxy(48,9);print("Cantidad") 
            gotoxy(58,9);print("Subtotal") 
            gotoxy(70,9);print("n->Terminar Venta)"+reset_color)

            follow = "s"
            line = 1
            while follow.lower() == "s":
                gotoxy(7,9+line);print(line)
                gotoxy(15,9+line);id_articulo = validar.solo_numeros("Error: Solo numeros",15,9+line)
                json_file_path = path + '/archivos/products.json'
                json_file = JsonFile(json_file_path)
                prods = json_file.find("id", id_articulo)
                if not prods:
                    gotoxy(24,9+line);print("Producto no existe")
                    time.sleep(1)
                    gotoxy(24,9+line);print(" "*20)
                    continue

                prods = prods[0]
                product = Product(prods["id"], prods["descripcion"], prods["precio"], prods["stock"])

                gotoxy(24,9+line);print(product.descrip)
                gotoxy(38,9+line);print(product.preci)

                qty = int(validar.solo_numeros("Error: Solo numeros",49,9+line))

                gotoxy(59,9+line);print(product.preci * qty)

                sale.add_detail(product, qty)
                gotoxy(76,4);print(round(sale.subtotal,2))
                gotoxy(76,5);print(round(sale.discount,2))
                gotoxy(76,6);print(round(sale.iva,2))
                gotoxy(76,7);print(round(sale.total,2))

                factura_encontrada["detalle"][0]["poducto"] = product.descrip
                factura_encontrada["detalle"][0]["precio"] = product.preci
                factura_encontrada["detalle"][0]["cantidad"] = qty

                gotoxy(74,9+line);follow = input() or "s"
                gotoxy(76,9+line);print(green_color+"✔"+reset_color)
                line += 1

            gotoxy(15,9+line);print(red_color+"Esta seguro de grabar la venta(s/n):")
            gotoxy(54,9+line);procesar = input().lower()
            if procesar == "s":
                gotoxy(15,10+line);print("😊 Venta Grabada satisfactoriamente 😊"+reset_color)
                json_file = JsonFile(path+'/archivos/invoices.json')
                invoices = json_file.read()
                if invoices:
                    invoices = json.loads(invoices)  
                    for factura in invoices:
                        if factura["factura"] == fact:
                            factura["Fecha"] = datetime.datetime.now().strftime("%Y-%m-%d") 
                            factura["cliente"] = cli.fullName()  
                            factura["subtotal"] = sale.subtotal  
                            factura["descuento"] = sale.discount  
                            factura["iva"] = sale.iva 
                            factura["total"] = sale.total  
                            factura["detalle"] = factura_encontrada["detalle"] 
                            break
                else:
                    invoices = []

                json_file.write(json.dumps(invoices, indent=4))
            else:
                gotoxy(20,10+line);print("🤣 Venta Cancelada 🤣"+reset_color)    
            time.sleep(2)
            input("enter")
        else:
            input("Factura no encontrada, presione enter")

        break

  def delete(self):
        while True:
            borrarPantalla()
            print('Actualizar datos de la factura.')
            fact = input("Ingresar el digito de factura, para actualizar los datos :").strip()
            if ' ' in fact or not fact.isdigit() or len(fact) != 1:
                print("numero de factura invalido.")
                time.sleep(2)
                continue
            fact = float(fact)
            json_file = JsonFile(path+'/archivos/invoices.json')
            clients_data = json_file.find("factura", fact)
            if not clients_data:
                print("se encontro factura.")
                time.sleep(2)
                continue
            
            factura_encontrada = clients_data[0]
            print()
            print('\033c', end='')
            gotoxy(2,1);print(green_color+"██"*50+reset_color)
            gotoxy(30,2);print(blue_color+"Registro de Venta")
            gotoxy(17,3);print(blue_color+Company.get_business_name())
            gotoxy(5,4);print(f"Factura#: {factura_encontrada['factura']} {' '*3} Fecha:{factura_encontrada['Fecha']}")
            gotoxy(66,4);print(" Subtotal: ", factura_encontrada["subtotal"])
            gotoxy(66,5);print(" Descuento: ", factura_encontrada["descuento"])
            gotoxy(66,6);print(" IVA     : ", factura_encontrada["iva"])
            gotoxy(66,7);print(" Total   : ", factura_encontrada["total"])
            gotoxy(10,6);print("Cliente: ", factura_encontrada["cliente"])
            gotoxy(2,8);print(green_color+"██"*50+reset_color)
            print()
            print(" enter o  esc")

            while True:
                if msvcrt.kbhit():
                    entrada = msvcrt.getch()
                    if entrada == b"\x1b":
                        print()
                        print("cancelada.")
                        time.sleep(1)
                        break

                    elif entrada == b"\r":
                        fact = float(fact)
                        json_file_path = path + '/archivos/invoices.json'
                        with open(json_file_path, 'r+') as file:
                            invoices = json.load(file)
                            for i, factura in enumerate(invoices):
                                if factura["factura"] == fact:
                                    del invoices[i]
                            file.seek(0)
                            json.dump(invoices, file, indent=4)
                            file.truncate()
                        break
            break
                                
        
  def consult(self):
    
    while True:
        borrarPantalla()
        print('Consultar factura.')
        print()
        invoice = input("Ingresar número de factura, para encontrar ").strip()
        if ' ' in invoice or not invoice.isdigit() or len(invoice) != 1:
            print("ingrese correctamente numero de la factura.")
            time.sleep(2)
            continue
          
        borrarPantalla()
        print('Consultando factura.')
        print()
        if invoice.isdigit():
            invoice = int(invoice)
            json_file = JsonFile(path + '/archivos/invoices.json')
            invoices = json_file.find("factura",invoice)
            if invoices:
                for fac in invoices:
                    for key, value in fac.items():
                        print(f"{key}: {value}")
                        
                    print(f"{'-' * 50}")
            else:
                print("La factura no existe.")
        else:
            json_file = JsonFile(path + '/archivos/invoices.json')
            invoices = json_file.read()
            print("Consulta de Facturas")
            for fac in invoices:
                for key, value in fac.items():
                    print(f"{key}: {value}")
                print(f"{'-' * 80}")

        input(f"Enter para continuar :")
        
        break

opc = ''
while opc != '4':
    borrarPantalla()
    menu_main = Menu("Menu Facturacion", [" 1) Clientes", " 2) Productos", " 3) Ventas", " 4) Salir"], 20, 10)
    opc = menu_main.menu()
    if opc == "1":
        opc1 = ''
        while opc1 != '5':
            borrarPantalla()
            menu_clients = Menu("Menu Clientes", [" 1) Ingresar", " 2) Actualizar", " 3) Eliminar", " 4) Consultar", " 5) Salir"], 10, 10)
            opc1 = menu_clients.menu()

            if opc1 == "1":
                borrarPantalla()
                crud_clients = CrudClients()
                crud_clients.create()

            elif opc1 == "2":
                borrarPantalla()
                crud_clients = CrudClients()
                crud_clients.update()

            elif opc1 == "3":
                borrarPantalla()
                crud_clients = CrudClients()
                crud_clients.delete()
                break
                    

            elif opc1 == "4":
                borrarPantalla()
                crud_clients = CrudClients()
                crud_clients.consult()
                     
    elif opc == "2":
        opc2 = ''
        while opc2 != '5':
            borrarPantalla()
            menu_products = Menu("Menu Productos", [" 1) Ingresar", " 2) Actualizar", " 3) Eliminar", " 4) Consultar", " 5) Salir"], 20, 10)
            opc2 = menu_products.menu()
            if opc2 == "1":
                borrarPantalla()
                crud_productos = CrudProducts()
                crud_productos.create()

            elif opc2 == "2":
                borrarPantalla()
                crud_productos = CrudProducts()
                crud_productos.update()
                
            elif opc2 == "3":
                borrarPantalla()
                crud_productos = CrudProducts()
                crud_productos.delete()
                   

            elif opc2 == "4":
                borrarPantalla()
                crud_productos = CrudProducts()
                crud_productos.consult()
                          
    elif opc == "3":
        opc3 = ''
        while opc3 != '5':
            borrarPantalla()
            sales = CrudSales()
            menu_sales = Menu("Menu Ventas", [" 1) Registro Venta", " 2) Modificar", " 3) Eliminar", " 4) Consultar", " 5) Salir"], 20, 10)
            opc3 = menu_sales.menu()
            if opc3 == "1":
                borrarPantalla()
                sales.create()
                  
            elif opc3 == "2":
                borrarPantalla()
                sales.update()
                           
            elif opc3 == "3":
                borrarPantalla()
                sales.delete()
                           
            elif opc3 == "4":
                borrarPantalla()
                sales.consult()
                        
        print("Regresando al menú Principal...")
        time.sleep(2)

borrarPantalla()
input("Presione una tecla para salir...")
borrarPantalla()