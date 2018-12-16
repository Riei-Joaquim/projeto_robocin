import numpy as np 
import cv2

cap = cv2.VideoCapture("Troca de goleiro.mp4")

def find_Seg_rob(frame):
    #intervalos
    min_amarelo = np.array([25,50,100])
    max_amarelo = np.array([50,220,255])
    min_rosa = np.array([120,70,85])
    max_rosa = np.array([255,255,255])
    min_verde = np.array([70,80,90])
    max_verde = np.array([105,180,190])
    min_azul = np.array([65,85,85])
    max_azul = np.array([110,220,220])
    quadros = []
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #segmentos amarelo
    mask1 = cv2.inRange(hsv_frame, min_amarelo, max_amarelo)
    _, contorno1, hierarquia1 = cv2.findContours(mask1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if(contorno1):
        for cnt1 in contorno1:
            if(40 < cv2.contourArea(cnt1)):
                x,y, w, h = cv2.boundingRect(cnt1)
                quadros.append((x,y,w,h))
    
    #segmentos rosa
        mask3 = cv2.inRange(hsv_frame, min_rosa, max_rosa)
        _, contorno3, hierarquia3 = cv2.findContours(mask3, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if(contorno3):
            for cnt3 in contorno3:
                if(40 < cv2.contourArea(cnt3)):
                    x,y, w, h = cv2.boundingRect(cnt3)
                    quadros.append((x,y,w,h))
    
    #segmentos verdes
    mask4 = cv2.inRange(hsv_frame, min_verde, max_verde)
    _, contorno4, hierarquia4 = cv2.findContours(mask4, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if(contorno4):
        for cnt4 in contorno4:
            if(cv2.contourArea(cnt4) > 40):
                x,y, w, h = cv2.boundingRect(cnt4)
                quadros.append((x,y,w,h))
    
    #segmentos azuis
    mask5 = cv2.inRange(hsv_frame, min_azul, max_azul)
    _, contorno5, hierarquia5 = cv2.findContours(mask5, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if(contorno5):
        for cnt5 in contorno5:
            if(cv2.contourArea(cnt5) > 65):
                x,y, w, h = cv2.boundingRect(cnt5)
                quadros.append((x,y,w,h))
    return quadros

def find_bola(frame):
    min_laranja = np.array([0,130,210])
    max_laranja= np.array([60,240,255])
    quadros = []
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #segmentos laranja
    mask2 = cv2.inRange(hsv_frame, min_laranja, max_laranja)
    _, contorno2, hierarquia2 = cv2.findContours(mask2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if(contorno2):
        for cnt2 in contorno2:
            if(10 < cv2.contourArea(cnt2)):
                x,y, w, h = cv2.boundingRect(cnt2)
                quadros.append((x,y,w,h))
    return quadros

def centro_robot(pontos, frame):
    centro = []
    mark = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    uniao = []
    for ele in pontos:
        x,y,w,h = ele
        medx = x + w//2
        medy = y + h//2
        centro.append((medx, medy))

    for ind1 in range(len(centro) -1):
        xat,yat = centro[ind1]
        medx = xat
        medy = yat
        if(mark[ind1] == 0):
            for ind2 in range(len(centro) -1):
                if(mark[ind2] == 0):
                    xi,yi = centro[ind2]
                    if((abs(xi- xat) <17)and(abs(yi- yat) <16)):
                        medx = (medx + xi)//2
                        medy = (medy +yi)//2
                        mark[ind2] = 1
            uniao.append((medx, medy))
    return uniao

def mostra_tracker_bola(regis, frame):
    for bol in regis:
        x, y, w, h = bol
        cv2.rectangle(frame, (x,y), (x+w, y+h),( 255, 0, 0), 2)
    
def escreve_texto(string, frame, x,y):
    texto = '{}'.format(string)
    fonte = cv2.FONT_ITALIC
    cv2.putText(frame, texto, (x-3,y-3), fonte, 0.5, (255, 255, 255), 1)

def mostra_tracker_robot(regis, frame):
    for rob in regis:
        x, y = rob
        cv2.rectangle(frame, (x-12,y-12), (x+16, y+16),( 0, 0, 255), 2)
        

def distancia(xa,ya,xb,yb):
    fat_pcm = 130/360
    dist_pixel = ((xa - xb)**2 + (ya - yb)**2)**0.5
    dist_real = dist_pixel*fat_pcm
    dist_real = round(dist_real, 2)
    return dist_real

def grafo_bola(trackbola, trackrobot,frame, cont_f):
    alt, larg,_ = frame.shape
    mat_vazia = np.zeros((alt, larg), dtype ="uint8")
    imagem_dist = cv2.merge([mat_vazia, mat_vazia, mat_vazia])
    imagem_vel = cv2.merge([mat_vazia, mat_vazia, mat_vazia])
    adj_bola = []
    fat_ft = 1/30
    fat_pcm = 130/360
    vel_bol = 0.0
    global medx
    global medy
    global dist_ant
    global bx
    global by
    if(cont_f == 0):
        dist_ant = np.array([0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0])

    if(len(trackbola) > 0):
        x,y,w,h = trackbola[0]
        medx = x + w//2
        medy = y + h//2
        if(cont_f == 0):
            bx = medx
            by = medy
        else:
            delx = distancia(medx,medy, bx, by)
            vel_bol = delx*fat_ft*fat_pcm
            vel_bol = round(vel_bol, 2)
            bx = medx
            by = medy
            
    cv2.circle(imagem_dist,(medx, medy), 4, (255,0,0), 2)
    cv2.circle(imagem_vel,(medx, medy), 4, (255,0,0), 2)
    n_velb = str(vel_bol)
    n_velb = n_velb + " cm/s"
    escreve_texto(n_velb, imagem_vel,medx-20,medy-10)
    adj_bola.append((medx,medy, 0, vel_bol))
    ind = 0

    for rob in trackrobot:
        xr, yr = rob
        cv2.line(imagem_dist, (medx,medy), (xr, yr),(255,0,0),2)
        cv2.circle(imagem_dist,(xr, yr), 5, (0,0,255), 2)

        cv2.circle(imagem_vel,(xr, yr), 5, (0,0,255), 2)
        dist = distancia(medx,medy,xr,yr)
        if(cont_f == 0):
            vel = 0.0
            dist_ant[ind] = dist
        else:
            dels = dist -dist_ant[ind]
            vel = dels*fat_ft*fat_pcm
            vel = round(vel,2)
            dist_ant[ind] = dist

        n_dist = str(dist)
        n_dist = n_dist + " cm"
        escreve_texto(n_dist, imagem_dist,xr-20,yr-10)
        n_vel = str(vel)
        n_vel = n_vel + " cm/s"
        escreve_texto(n_vel, imagem_vel,xr-20,yr-10)
        ind += 1

    cv2.imshow("distancia ate a bola", imagem_dist)
    cv2.imshow("velocidade dos objetos ", imagem_vel)
    return adj_bola

def main():     
    cont_f = 0
    while(True):
        t_frame, frame = cap.read()
        if(t_frame):
            trackseg = find_Seg_rob(frame)
            trackrobot = centro_robot(trackseg,frame) 
            trackbola = find_bola(frame)
            mostra_tracker_bola(trackbola,frame)
            mostra_tracker_robot(trackrobot,frame)
            cv2.imshow("tracker em video", frame)
            dados = grafo_bola(trackbola,trackrobot,frame, cont_f)
            cont_f += 1
        if cv2.waitKey(10) & 0xff == ord('p'):
            while(True):
                if cv2.waitKey(10) & 0xff == ord('p'):
                    break

        if cv2.waitKey(10) & 0xff == ord('q'):
             break

    cap.release()
    cv2.destroyAllWindows()

main()