import Stixai
import easygui as gui
import random
import pygame
import time
#print 'all xpose'

#print 'pose'
pygame.init()
screen = pygame.display.set_mode([640, 480])
screen.fill([255, 255, 255])
pygame.display.flip()
reptimes = 0
#print 'init comp'

def begin():
    ins = open('in.txt', 'r')
    outs = open('out.txt', 'r')
    il = ins.readlines()
    ol = outs.readlines()
    ins.close()
    outs.close()
    #print il
    #print ol
    ilx = ''
    olx = ''
    excluded = []
    for i in il:
        #print 'i: ' + i
        if len(i) == 6:
            ilx = str(ilx) + str(i)
        else:
            excluded.append(il.index(i))
        
    for i in ol:
        #print 'i: ' + i
        if len(i) == 6 and not ol.index(i) in excluded:
            olx = str(olx) + str(i)
    ilist = ilx.split('\n')
    olist = olx.split('\n')
    #print ilist
    #print olist
    ilist.pop()
    olist.pop()
    #print ilist
    #print olist
    for i in ilist:
        x = i
        #print 'i: ' + i
        if i[3] == '-':
            x = i[0:3] + '0' + i[5]
        elif int(i[3]) > 3:
            x = i[0:3] + '3' + i[4]
        if i[4] == '-':
            x = i[0:5] + '0'
        elif int(i[4]) > 3:
            x = i[0:4] + '3'
        fx = x
        x = []
        for n in fx:
            x.append(n)
        #print x
        if x[0:3] == ['a','t','k']:
            if int(x[3]) < 2:
                x[3] = '2'
            if int(x[4]) > 1:
                x[4] = '1'
        else:
            if int(x[3]) != 2:
                x[3] = '2'
            if int(x[4]) != 3:
                x[4] = '3'
        ilist[ilist.index(i)] = ''.join(x)
        
    for i in olist:
        #print 'i: ' + i
        x = i
        #print x
        if i[3] == '-':
            x = i[0:3] + '0' + i[5]
        elif int(i[3]) > 3:
            x = i[0:3] + '3' + i[4]
        if i[4] == '-':
            x = i[0:5] + '0'
        elif int(i[4]) > 3:
            x = i[0:4] + '3'

        fx = x
        x = []
        for n in fx:
            x.append(n)
        #print x
        if x[0:3] == ['a','t','k']:
            if int(x[3]) < 2:
                x[3] = '1'
            if int(x[4]) > 1:
                x[4] = '2'
        else:
            if int(x[3]) != 0:
                x[3] = '0'
            if int(x[4]) != 1:
                x[4] = '1'
        olist[olist.index(i)] = ''.join(x)
        
    return [ilist, olist]

def render(hands):

    hpos = [[205, 33], [340, 33], [340, 296], [205, 296]]
    screen.blit(pygame.image.load('Background.png'), [0,0])
    for i in hpos:
        #print '1: ' + str(hpos.index(i))
        #print '2: ' + str(hands[hpos.index(i)])
        if int(str(hands[hpos.index(i)])) < 0:
            screen.blit(pygame.image.load('0f.png'), i)
        else:
            screen.blit(pygame.image.load(str(hands[hpos.index(i)]) + 'f.png'), i)

    pygame.display.flip()
    
def evaluate(action, hands):
    global reptimes
    #print action
    #action syntax: action (3 chars), used hand (in hand list, 0-3), recipient hand (in hand list, 0-3)
    #atk02
    a = action[0] + action[1] + action[2]
    hn = action[3] + action[4]
    h = str(hands[int(hn[0])]) + str(hands[int(hn[1])])
    ra = hands[int(hn[1])]
    ri = hands[int(hn[0])]
    rinum = int(hn[0])
    ranum = int(hn[1])
    evaluated = False
    #print a
    if a == 'atk':#attack
        if int(h[0]) + int(h[1]) < 6 and int(h[0]) != 0 and int(h[1]) != 0:
            evaluated = True
            ra = int(h[0]) + int(h[1])
            ri = int(h[0])
            reptimes = 0
            #print ri
            #print ra
    elif a == 'swt':#switch
        if int(h[0]) != 0 and int(h[1]) != 0 and reptimes < 3:
            evaluated = True
            ha = ri
            hb = ra
            ri = hb
            ra = ha
            reptimes += 1
    elif a == 'div':#divide
        if reptimes < 3:
            evaluated = True
            Sum = ri + ra
            div = int(round(Sum / 2))
            if Sum % 2 != 0:
                ri = div + 1
                ra = div
            else:
                ri = div
                ra = div
            reptimes += 1
        


    hF = []
    ctr = 0
    for i in hands:
        if ctr == rinum:
            hF.append(ri)
        elif ctr == ranum:
            hF.append(ra)
        else:
            hF.append(i)
        #print hF
        ctr += 1
            
        

    return [evaluated, hF]

def cwin(hands):
    fH = []
    for i in hands:
        if i == 5:
            fH.append(0)
        else:
            fH.append(i)
        #print 'fh: ' + str(fH)
    win = 'none'
    winBool = False
    if fH[0] <= 0 and fH[1] <= 0:
        win = 'You'
        winBool = True
    elif fH[2] <= 0 and fH[3] <= 0:
        win = 'StixAI'
        winBool = True
    return [fH, win, winBool]

def translate(action, human):
    if action[0:3] == 'atk':
        if human:
            tact = action[0:3] + str(int(action[3]) - 2) + str(int(action[4]) + 2)
        else:
            tact = action[0:3] + str(int(action[3]) + 2) + str(int(action[4]) - 2)
    else:
        if human:
            tact = action[0:3] + str(int(action[3]) - 2) + str(int(action[4]) - 2)
        else:
            tact = action[0:3] + str(int(action[3]) + 2) + str(int(action[4]) + 2)
    #print 'tact' + tact
    return tact

def chooser():
    ranchoose = ['02', '12', '03', '13']
    acts = ['atk', 'swt', 'div']
    act = random.choice(acts)
    if act == 'atk':
        anum = random.choice(ranchoose)
    else:
        anum = '23'
    return act + anum

def main():
    global reptimes
    hands = [1, 1, 1, 1]
    #pose.servset([hands[0],hands[1]])
    #hands = [ai right, ai left, human right, human left]
    data = begin()
    ins = data[0]
    outs = data[1]
    #print ins
    #print outs
    winner = None
    ai = Stixai.ai(ins, outs)
    bchands = ['31', '30', '21', '20']
    
    if len(outs) == 0:
        pact = random.choice(['atk', 'swt', 'div']) + str(random.randint(0, 3)) + str(random.randint(0, 3))
    else:
        pact = random.choice(outs)
    
    running = True
    while running:

        vres = 0
        evd = False
        while not evd and vres <= 100:
            cpu_act = ai.get_act(pact, vres)
            evdata = evaluate(cpu_act, hands)
            evd = evdata[0]
            hands = evdata[1]
            #print evdata
            if evd:
                ins.append(translate(cpu_act, False))
                outs.append(translate(pact, True))
            else:
                vres += 1
            #print vres
        if vres > 100:
            c = 0
            while c <= 100:
                evdata = evaluate(chooser(), hands)
                evd = evdata[0]
                hands = evdata[1]
            if c > 100:
                win = 'You'
                break
        
        cwinv = cwin(hands)
        render(hands)
        win = cwinv[1]
        wbool = cwinv[2]
        handsF = cwinv[0]
        hands = handsF
        #print 'Player:'
        #print 'Left: ' + str(hands[3])
        #print 'Right: ' + str(hands[2])
        #print 'StixAI:'
        #print 'Left: ' + str(hands[1])
        #print 'Right: ' + str(hands[0])
        render(hands)
        #pose.servset([hands[0],hands[1]])
        time.sleep(1)
        
        if wbool:
            break
        evd = False
        again = False
        while not evd:
            if again:
                gui.msgbox('Invalid entry due to rules and stuffz. Please try again or forfeit if you are raging.')
            achoice = gui.indexbox('Please choose an action. Cancelling will result in you forfeiting the game.', choices=['Forfeit', 'Attack', 'Switch', 'Divide'])
            #print achoice
            if achoice == 0:
                win = 'Stixai'
                wbool = True
                running = False
                break
            elif achoice == 1:
                bchoice = gui.indexbox('Select which hand you want to use.', choices=['Left -> Left', 'Left -> Right', 'Right -> Left', 'Right -> Right'])
                act = 'atk' + bchands[bchoice]
            elif achoice == 2:
                act = 'swt' + '23'
            elif achoice == 3:
                act = 'div' + '23'
                
            evr = evaluate(act, hands)
            evd = evr[0]
            hands = evr[1]
            if not evd:
                again = True
        if wbool:
            break
        pact = act
        cwinv = cwin(hands)
        outs[len(outs) - 1] = translate(pact, True)
        if wbool:
            break
        
        win = cwinv[1]
        wbool = cwinv[2]
        handsF = cwinv[0]
        hands = handsF
        if wbool:
            break
        #print 'Player:'
        #print 'Left: ' + str(hands[3])
        #print 'Right: ' + str(hands[2])
        #print 'StixAI:'
        #print 'Left: ' + str(hands[1])
        #print 'Right: ' + str(hands[0])
        render(hands)
        #pose.servset([hands[0],hands[1]])
        time.sleep(1)
        

    gui.msgbox(win + ' won.')
    insf = open('in.txt', 'w')
    outsf = open('out.txt', 'w')
    for i in ins:
        print >> insf, i
    for i in outs:
        print >> outsf, i
    insf.close()
    outsf.close()
    
        
            
#print 'func def'            


main()
#print 'done'

#pose.servset([0,0])
pygame.quit()
