import subprocess
import cv2

def escreve_texto(string, imagem, x,y):
    texto = '{}'.format(string)
    fonte = cv2.FONT_ITALIC
    cv2.putText(imagem, texto, (x-3,y-3), fonte, 1, (255, 0, 0), 2)

def trata_string(entrada):
    dado = str(entrada)
    trat = ""
    subreg =[]
    tevep = False
    for i in range(len(dado) -1):
        if(dado[i] == "]"):
            tevep = False
            subreg.append(trat)
            trat = ""

        if(tevep):
            trat+= dado[i]

        if(dado[i] == "["):
            tevep = True
    return subreg

def operador_cl(end_img):
    agr_img = "--image=" + end_img
    outclassifier = subprocess.check_output(["python3.6", "-m", "scripts.label_image", "--graph=tf_files/retrained_graph.pb",  agr_img])
    return outclassifier

def classificador():
    enderecos = ["tf_files/flower_photos/tulips/teste1_3d.jpg",
                "tf_files/flower_photos/tulips/teste2_3d.jpg", 
                "tf_files/flower_photos/daisy/teste1logo.jpg",
                "tf_files/flower_photos/daisy/teste2logo.jpg",
                "tf_files/flower_photos/daisy/teste3logo.jpg"]
    
    load_imgs = []
    for im in enderecos:
        tmp = cv2.imread(im, 1)
        load_imgs.append(tmp)

    for j in range(len(enderecos)):
        end_at = enderecos[j]
        analise = operador_cl(end_at)
        res = trata_string(analise)
        orix = 10
        oriy = 30
        escreve_texto("pontuacao gerada na rede neural:",load_imgs[j],orix,oriy)
        oriy += 35
        for dado in res:
            escreve_texto(dado,load_imgs[j],orix,oriy)
            oriy += 25
        nome_ab = "imagem analisada "
        nome_ab += str((j+1))
        cv2.imshow(nome_ab, load_imgs[j])
        

def main():
    
    classificador()

    while(True):
        if cv2.waitKey(10) & 0xff == ord('q'):
            cv2.destroyAllWindows()
            break

main()