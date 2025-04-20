marcos_libres = [0x0,0x1,0x2]
reqs = [ 0x00, 0x12, 0x64, 0x65, 0x8D, 0x8F, 0x19, 0x18, 0xF1, 0x0B, 0xDF, 0x0A ]
segmentos =[ ('.text', 0x00, 0x1A),
             ('.data', 0x40, 0x28),
             ('.heap', 0x80, 0x1F),
             ('.stack', 0xC0, 0x22),
           ]

def procesar(segmentos, solicitudes, libres):
    TAMANIO_PAGINA = 0x10
    asignaciones = {}
    uso = {}
    reloj = 0
    salida = []

    for direccion in solicitudes:
        reloj += 1

        if not any(inicio <= direccion < inicio + longitud for _, inicio, longitud in segmentos):
            salida.append((direccion, 0x1FF, "Segmention Fault"))
            continue

        pagina = direccion >> 4  
        desplazamiento = direccion & 0xF  

        if pagina in asignaciones:
            marco_actual = asignaciones.get(pagina)
            uso[pagina] = reloj
            salida.append((direccion, (marco_actual << 4) + desplazamiento, "Marco ya estaba asignado"))
            continue

        if libres:
            nuevo_marco = libres.pop(0)
            asignaciones[pagina] = nuevo_marco
            uso[pagina] = reloj
            salida.append((direccion, (nuevo_marco << 4) + desplazamiento, "Marco libre asignado"))
        else:
            victima = min(uso.items(), key=lambda x: x[1])[0]
            marco_viejo = asignaciones.pop(victima)
            uso.pop(victima)
            asignaciones[pagina] = marco_viejo
            uso[pagina] = reloj
            salida.append((direccion, (marco_viejo << 4) + desplazamiento, "Marco asignado"))

    return salida



def print_results(results):
    for result in results:
        print(f"Req: {result[0]:#0{4}x} Direccion Fisica: {result[1]:#0{4}x} Acción: {result[2]}")

if __name__== '__main__':
    results = procesar(segmentos, reqs, marcos_libres)
    print_results(results)