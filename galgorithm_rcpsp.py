# -*- coding: UTF-8 -*-
import string
import random
import copy
import sys
import time
from numpy.random import choice


rn = 0  # 资源种类
tasks = []
resourceAvailabilities = {}
FtimeFit = []


def clearLine(e):
    """
    获取数据
    :param e:
    :return:
    """
    te = len(e)
    i = 0
    v = []
    flag = 0
    word = ''
    while i < te:
        if e[i] == ' ':
            if flag == 1:
                # 插入非否定值
                v.append(int(word))
                word = ''
                flag = 0
                i = i + 1
            else:
                i = i + 1
        else:
            word = word + e[i]
            flag = 1
            i = i + 1
    if word:
        v.append(int(word))

    return v


def load(instancia):
    """
    加载数据
    :param instancia:
    """
    global rn
    arq = open(instancia, 'r')
    text = arq.read()
    lines = string.split(text, '\n')
    nt = 0

    while nt < numTasks:
        # 选择部分数据
        e1 = lines[offsetIni + nt]
        e2 = lines[offsetIni + offsetFim + nt]
        l1 = clearLine(e1)
        l2 = clearLine(e2)
        h1 = len(l1)
        h2 = len(l2)
        # 任务NR，后继者，资源，任务持续时间
        t = {'NR': l1[0],
             'Predecessors': [],
             'Sucessors': l1[3:h1],
             'TimeDuration': l2[2]}
        r = {}
        for h in range(3, h2):
            r['R' + str(h - 2)] = l2[h]
        t.update(r)
        tasks.append(t)
        nt = nt + 1

    # 资源量R1 R2 R3 R4
    e3 = lines[offsetResource]
    l3 = clearLine(e3)
    rn = len(l3)
    for h in range(rn):
        resourceAvailabilities['R' + str(h + 1)] = l3[h]
    generatePredecessors()


def getActivity(num):
    """
        获取活动
    :param num:
    :return:
    """
    for ativ in tasks:
        if ativ['NR'] == num:
            return ativ


def isPredecessor(t, pt):
    """
        判断紧前活动。依据：pt的紧后活动列表是否存在t['NR']值
    :param t:
    :param pt:
    :return:
    """
    try:
        i = pt['Sucessors'].index(t['NR'])
    except ValueError:
        return -1
    else:
        return 1


def verifyAlreadyPredecessorsScheduled(predecessors, s):
    """
    判断当前活动的紧前活动是否都已经加入调度中
    :param predecessors:
    :param s:
    :return:
    """
    for p in predecessors:
        try:
            i = s.index(p)
        except ValueError:
            return -1
        else:
            pass

    return 1


def getEarliestEndingPredecessor(j, et):
    """
    获取紧前活动最早完成时间EndTime
    :param j:
    :param et:
    :return:
    """
    pft = {'NR': 0, 'TimeEnd': 0}

    for p in j['Predecessors']:
        for a in et:
            if p == a['NR']:
                if a['TimeEnd'] > pft['TimeEnd']:
                    pft = a
    return pft['TimeEnd']


def generatePredecessors():
    """
        创建紧前列表,时间复杂度O(n*2)
    """
    pred = []
    i = 0
    while i < numTasks:
        for t2 in tasks:
            if isPredecessor(tasks[i], t2) == 1:
                pred.append(t2['NR'])
        tasks[i]['Predecessors'] = pred
        pred = []
        i = i + 1


def selectElegibleActivities(s, d, t):
    # 获取合格的活动集合，活动列表s分割任务集合t，删除部分存入集合d中
    length = len(t)
    count = 0
    listpop = []
    while count < length:
        cp = 0
        # 试图判断t[count]所有紧前活动是否存在s列表中
        for p in t[count]['Predecessors']:
            try:
                i = s.index(p)  # 试图判断p活动是否存在s列表中
            except ValueError:
                break
            else:
                cp = cp + 1
        # 若是，则将该t[count]活动加入集合d，d初始化为空列表
        if cp == len(t[count]['Predecessors']):
            d.append(t[count])
            listpop.append(t[count])
        count = count + 1
    # 活动被处理
    for pop in listpop:
        t.remove(pop)


def getRandomElegibleActivitie(d):

    if not d:
        return -1
    else:
        ra = random.choice(d)
        d.remove(ra)
        return ra


# 未调用
def getShortesElegibleActivitie(d):
    orderedElegiblesActivities = orderActivities(d, 1)
    activ = orderedElegiblesActivities.pop()
    for a in d:
        if activ['NR'] == a['NR']:
            try:
                i = d.index(a)  # 交叉
            except ValueError:
                break
            else:
                pass
            act = d.pop(i)
            return act
    return -1


# 未调用
def orderActivities(Dg, asc):
    """
        活动排序
    :param Dg:
    :param asc:
    :return:
    """
    popElitist = sorted(Dg, key=lambda k: k['TimeDuration'])
    if asc:
        return popElitist
    else:
        popElitist.reverse()
        return popElitist


def updateResourceUsageTime(demand, resourceUsageTime, inst):
    """
        及时更新资源，inst时间加上所需资源量以更新resourceUsageTime
    :param demand:
    :param resourceUsageTime:
    :param inst:
    """
    for resource, amount in resourceUsageTime[inst].iteritems():
        if resource in demand:
            resourceUsageTime[inst][resource] = resourceUsageTime[inst][resource] + \
                demand[resource]


def verifyResourceAvailabilities(demand, resourceUsageTime, inst):
    """
    比较资源量: resourceUsageTime中inst时刻的资源使用量 + 所需要的资源是否大于资源限制resourceAvailabilities
    :param demand:
    :param resourceUsageTime:
    :param inst:
    :return:
    """
    for resource, amount in resourceUsageTime[inst].iteritems():
        if resource in demand:
            if resourceUsageTime[inst][resource] + \
                    demand[resource] > resourceAvailabilities[resource]:
                return -1
    return 1


def allocatingActivityOnTimeLine(j, resourceUsageTime, inst):
    """
        t时间增加使用资源及获取TimeEnd
    :param j:
    :param resourceUsageTime:
    :param inst:
    :return:
    """
    isScheduled = False
    timeStart = inst
    reserveResourceInTime = []
    countTime = 0
    TimeEnd = 0
    limit = 0
    break_flag = False
    while isScheduled == False:
        limit = timeStart + j['TimeDuration']
        countTime = timeStart
        # 验证是否可以分配活动运行时所需的所有资源
        for t in range(timeStart, limit):
            # 如果它在resourceUsageTime中不存在，则意味着从现在起不再分配资源
            if t not in resourceUsageTime:
                rd = dict()
                for r in range(1, rn + 1):
                    rd['R' + str(r)] = 0
                resourceUsageTime[t] = rd
                updateResourceUsageTime(j, resourceUsageTime, t)
                countTime = countTime + 1
            # 验证此特定时刻的资源可用性, 如果可用，插入到列表中
            elif verifyResourceAvailabilities(j, resourceUsageTime, t) == 1:
                reserveResourceInTime.append(t)
                countTime = countTime + 1
            else:
                break_flag = True

        if countTime == limit:
            for t in reserveResourceInTime:
                updateResourceUsageTime(j, resourceUsageTime, t)
            isScheduled = True
            TimeEnd = timeStart + j['TimeDuration']
        else:
            countTime = 0
            timeStart = timeStart + 1
    if break_flag:
        TimeEnd = -1
    return TimeEnd


def SGS():
    """
        Serial Schedule Generation Scheme
        生成与选择后代基因
    :return:
    """
    tp = []  # 要处理的任务集合
    Dg = []  # 可供选择的活动集合
    Sg = []  # 已选择的活动
    Rkt = []  # t时间的可用资源的数量
    F = []  # 活动结束时间集合
    g = len(tasks)  # 工程量
    et = []  # 结束时间
    #etc = []
    resourceUsageTime = {}  # 可用时间资源
    individual = {}  # 实施中的问题
    tp = copy.deepcopy(tasks)

    # 活动处理
    task = tp.pop(0)
    et.append({'NR': task['NR'], 'TimeEnd': 0})
    # etc.append(0)
    Sg.append(task['NR'])
    F.append(1)
    # F.append(-2) # 首个虚节点为-2时引用
    rd = dict()
    for r in range(1, rn + 1):
        rd['R' + str(r)] = 0
    resourceUsageTime[0] = rd
    break_flag = False
    i = 1
    while i < g:
        # 选择活动
        selectElegibleActivities(Sg, Dg, tp)
        # Dg中随机选择一个活动j
        j = getRandomElegibleActivitie(Dg)
        # 创建函数消耗的资源
        # 为了确定最早完成时间ES，0,4,10...循环生成最大值，最后赋值给Cost，而忽视资源
        #etc.append({'NR': j['NR'], 'TimeMaxPredecessor': getEarliestEndingPredecessor(j, et)})
        ES = getEarliestEndingPredecessor(j, et)
        # et：活动NR的最早完成时间对NR，TimeEnd；
        # 执行结束时间，活动和资源的更新
        minJ = allocatingActivityOnTimeLine(j, resourceUsageTime, ES)
        if minJ == -1:
            break_flag = True
            break
        et.append({'NR': j['NR'], 'TimeEnd': minJ})
        # 计算结束时间放入集合
        F.append(et[-1])
        # 加入已选择活动集合Sg
        Sg.append(j['NR'])
        i = i + 1
    if break_flag:
        individual = {}
    else:
        individual['Chromossome'] = Sg
        individual['Cost'] = F[-1]['TimeEnd']
    return individual


def generatePopulation(n):
    """
        初始化种群
    :param n:
    :return:
    """
    i = 0
    m = 0
    max = 2  # 个体生成最高循环次数限制
    popu = []
    individual = {}
    while i < n:
        individual = SGS()
        if m != max:
            if not len(individual) and exsistsChromossome(
                    individual, popu) == 1:
                m = m + 1
                continue
            else:
                popu.append(SGS())
                m = 0
                i = i + 1
        else:
            return popu
    return popu


def exsistsChromossome(chromossome, population):
    """
    确保不会有相同染色体的个体
    :param chromossome:
    :param population:
    :return:
    """
    for ind in population:
        if chromossome['Chromossome'] == ind['Chromossome']:
            return 1
    return -1


def classifyCandidates(pop):
    """
        执行时间成本，升序排序
    :param pop:
    :return:
    """
    popElitist = sorted(pop, key=lambda k: k['Cost'])
    return popElitist


def selectsBestParents(pop, txSlection):
    """
    挑选精英父代
    :param pop:
    :param txSlection:
    :return:
    """
    poplength = len(pop)
    popCondidates = classifyCandidates(pop)
    selectQuantity = ((poplength * txSlection) / 2)
    # selectQuantity = ((poplength * txSlection) / 100)
    elit = popCondidates[0:selectQuantity]
    return elit


def crossover(ind1, ind2, candidates, qp):
    """

    :param ind1:
    :param ind2:
    :param candidates:
    :param qp:
    """
    pointer = 0
    threshold = 0
    chromossome1 = []
    chromossome2 = []
    son1 = {}
    son2 = {}
    lenInd1 = len(ind1['Chromossome'])
    lenInd2 = len(ind2['Chromossome'])
    listrandom = []
    offset = lenInd1 / (qp + 1)
    residual = lenInd1 % (qp + 1)
    set = 0

    #listrandom = range(0,lenInd1)
    #pointer =  random.choice(listrandom)

    if lenInd1 == lenInd2:
        # gerando filhos
        for i in range(1, qp + 2):
            # print 'i: ', i, 'offset: ', offset, 'pointer: ' , pointer
            threshold = (i * offset)

            if (i % 2) == 1:
                chromossome1 += ind1['Chromossome'][pointer:threshold]
                chromossome2 += ind2['Chromossome'][pointer:threshold]
                pointer = threshold
            else:
                chromossome1 += ind2['Chromossome'][pointer:threshold]
                chromossome2 += ind1['Chromossome'][pointer:threshold]
                pointer = threshold

        if residual > 0:
            if ((threshold + residual) % 2) == 1:
                chromossome1 += ind1['Chromossome'][pointer:threshold + residual]
                chromossome2 += ind2['Chromossome'][pointer:threshold + residual]
            else:
                chromossome1 += ind2['Chromossome'][pointer:threshold + residual]
                chromossome2 += ind1['Chromossome'][pointer:threshold + residual]
    else:
        print 'Paraents gene diferente!'
        exit(1)

    son1['Chromossome'] = chromossome1
    son2['Chromossome'] = chromossome2

    candidates.append(son1)
    candidates.append(son2)


def crossoverWithBestParents(bestP, pop, candidates, qp):
    """

    :param bestP:
    :param pop:
    :param candidates:
    :param qp:
    """
    i = 1
    j = 0
    lengthBP = len(bestP)
    lengthPOP = len(pop)

    while i < lengthBP - 1:
        j = 1
        while j < lengthPOP - 2:
            crossover(bestP[i], pop[j], candidates, qp)
            j = j + 1
        i = i + 1

# 未调用


def crossoverPopulation(pop, candidates, qp):
    """
    交叉变异
    :param pop:
    :param candidates:
    :param qp:
    """
    i = 1
    j = 0
    length = len(pop)

    while i < length - 1:
        j = 1
        while j < length - 2:
            crossover(pop[i], pop[j], candidates, qp)
            j = j + 1
        i = i + 1


def mutation(individual, candidates, probability):

    mutant = copy.deepcopy(individual)
    length = len(mutant['Chromossome'])
    aux = 0
    candidate = {}

    i = 1  # G
    while i < length - 2:
        if choice(2, p=[1 - probability, probability]):
            #chromossome.vect[x] = random_integers(1, Solution.solution_size)
            '''print 'mutation:'
            print 'Gene1: ', mutant['Chromossome'][i]
            print 'Gene2: ', mutant['Chromossome'][i+1]
            print mutant['Chromossome']'''
            aux = mutant['Chromossome'][i + 1]
            mutant['Chromossome'][i + 1] = mutant['Chromossome'][i]
            mutant['Chromossome'][i] = aux

            # print mutant['Chromossome']
        i = i + 1
    candidate['Chromossome'] = mutant['Chromossome']

    candidates.append(candidate)


def mutaitonPopulation(pop, candidates, probability):
    for ind in pop:
        mutation(ind, candidates, probability)


def hasRepeatedGene(chromossome):
    for gene in chromossome['Chromossome']:
        if chromossome['Chromossome'].count(gene) > 1:
            return 1
    else:
        return -1


def evaluationCandidate(candidate):
    if hasRepeatedGene(candidate) == 1:
        return None
    Sg = []
    F = []
    g = len(tasks)
    et = []
    resourceUsageTime = {}
    individual = {}
    task = getActivity(candidate['Chromossome'][0])
    et.append({'NR': task['NR'], 'TimeEnd': 0})
    Sg.append(task['NR'])
    F.append(1)
    rd = dict()
    for r in range(1, rn + 1):
        rd['R' + str(r)] = 0
    resourceUsageTime[0] = rd

    i = 1
    while i < g:
        # 从基因中获取第二个活动j
        j = getActivity(candidate['Chromossome'][i])

        # 时序约束：用已处理活动集合Sg校验当前活动j的紧前活动是否都已经加入调度
        if verifyAlreadyPredecessorsScheduled(j['Predecessors'], Sg) == -1:
            return None

        # 算法核心：每次轮训当前活动j的所有紧前活动的最早完成时间，获取其的EndTime
        ES = getEarliestEndingPredecessor(j, et)

        # 资源约束：更新t时刻资源使用量，完成该活动j的最早完成时间minJ=TimeEnd
        minJ = allocatingActivityOnTimeLine(j, resourceUsageTime, ES)

        et.append({'NR': j['NR'], 'TimeEnd': minJ})
        F.append(et[-1])
        Sg.append(j['NR'])
        i = i + 1

    individual['Chromossome'] = Sg
    individual['Cost'] = F[-1]['TimeEnd']

    # 生成时序Endtime列表
    if not FtimeFit:
        FtimeFit.append(F)
    elif F[-1]['TimeEnd'] < FtimeFit[-1][-1]['TimeEnd']:
        del FtimeFit[:]
        FtimeFit.append(F)
    elif F[-1]['TimeEnd'] == FtimeFit[-1][-1]['TimeEnd']:
        FtimeFit.append(F)
    else:
        pass

    return individual


def selectsCandidates(candidatesFit, numberpopulation):
    """
    按最短时间排序后，选择前numberpopulation个个体为新一代newGeneration
    :param candidatesFit:
    :param numberpopulation:
    :return:
    """
    classifiedList = classifyCandidates(candidatesFit)
    if numberpopulation < len(candidatesFit):
        selectedCandidates = classifiedList[0:numberpopulation]
    else:
        print "Num of individual can be created less than numpopulation given"
        return classifiedList
    return selectedCandidates


def global_arg(numtasks):
    global num_tasks, offsetFim, offsetResource, numTasks, offsetIni
    num_tasks = numtasks
    offsetFim = num_tasks + 4
    offsetIni = 18
    offsetResource = offsetIni + num_tasks * 2 + 7
    numTasks = num_tasks


# 遗传算法入口
def ga_processor(numtasks, num_pop, num_pot, tx_slt, num_iter, inst_file):
    global_arg(numtasks)
    numberpopulation = num_pop
    numberpoints = num_pot
    txSlection = tx_slt
    numberInteration = num_iter
    instancia = inst_file
    load(instancia)
    txMutation = 0.1  # 百分之一突变率
    Generations = []
    numberGeneration = 0
    newGeneration = []
    candidates = []
    candidatesFit = []
    counterIteration = 0
    bestFitnessNow = 0

    population = generatePopulation(numberpopulation)
    if not population:
        return -1, -1
    # Generation = [{'NrGeneration': numberGeneration, 'Population': population}]
    bestParents = selectsBestParents(population, txSlection)
    bestFitness = bestParents[0]['Cost']
    timeBegin = time.clock()

    while counterIteration <= numberInteration:
        numberGeneration = numberGeneration + 1

        # 从以前的种群中选择精英父代
        bestParents = selectsBestParents(population, txSlection)
        population = generatePopulation(
            numberpopulation - len(bestParents))  # 产生新的后代
        population = population + bestParents

        # 交叉、变异遗传进化过程
        # crossoverPopulation(population, candidates, numberpoints)
        crossoverWithBestParents(
            bestParents,
            population,
            candidates,
            numberpoints)
        mutaitonPopulation(population, candidates, txMutation)

        # 生成并选择合适的候选
        for ind in candidates:
            candidate = evaluationCandidate(ind)
            if candidate is None:
                pass
            else:
                candidatesFit.append(candidate)
        newGeneration = selectsCandidates(candidatesFit, numberpopulation)
        if newGeneration:
            # 计数器迭代
            bestFitnessNow = newGeneration[0]['Cost']
            if bestFitnessNow >= bestFitness:
                counterIteration = counterIteration + 1
            else:
                print(
                    'Geration:',
                    numberGeneration,
                    ' Antigo:',
                    bestFitness,
                    ' Novo:',
                    bestFitnessNow)
                bestFitness = bestFitnessNow
                counterIteration = 0
        print 'time', time.clock()

    return newGeneration[0], FtimeFit[0]


if __name__ == "__main__":
    numtasks = 7
    num_pop = 3
    num_pot = 2
    tx_slt = 2
    num_iter = 10
    inst_file = 'teste77.sm'
    ga_processor(numtasks, num_pop, num_pot, tx_slt, num_iter, inst_file)
