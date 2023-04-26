import os
import random
import time
from typing import Dict, List, Tuple
from .GenerateYaml import generate
from .TrafficAllocate import TrafficAllocate


class Random:
    def __init__(self, maxPods: int, machine: int, U: int, D: int):
         
Pod数量、最大机器数量、U、D 
        self.MaxPods = maxPods
        self.machines = machine
        self.UM = U
        self.DM = D
        self.UD = (U, D)
        self.Nodes = ['skv-node2', 'skv-node3', 'skv-node4',  'skv-node6', 'skv-node7']
        random.shuffle(self.Nodes)
        self.Nodes = self.Nodes[:machine]

    def get_result(self) -> Dict[str, List[int]]:
        result: Dict[str, List[int]] = {}
        for i in self.Nodes:
            result[i] = [0, 0]

        for i in range(self.UM):
            time.sleep(random.random() / 10)
            result[self.Nodes[random.randint(0, len(self.Nodes) - 1)]][0] += 1
        for i in range(self.DM):
            time.sleep(random.random() / 10)
            result[self.Nodes[random.randint(0, len(self.Nodes) - 1)]][1] += 1
        return result

    def Localize(self):
        result = self.get_result()
        print(result)
        generate('./Scheduler/wrk-nginx.yaml', './Scheduler/yaml_file/', result, self.UD[0], self.UD[1], self.machines)
        os.system('kubectl apply -f ./Scheduler/yaml_file/')
    def TrafficAllocation(self):
        TA = TrafficAllocate()
        TA.ExecuteNode()


class baseline:
    def __init__(self, maxPods: int, machine: int, U: int, D: int):
         
Pod数量、最大机器数量、U、D 
        self.MaxPods = maxPods
        self.machines = machine
        self.UM = U
        self.DM = D
        self.UD = (U, D)
        self.Nodes = ['skv-node2', 'skv-node3', 'skv-node4',  'skv-node6', 'skv-node7']
        random.shuffle(self.Nodes)
        self.Nodes = self.Nodes[:machine]

    def get_result(self) -> Dict[str, List[int]]:
        UM_quotas, DM_quotas = 0, 0
        if self.MaxPods % 2 == 1:
            if self.UM > self.DM:
                UM_quotas = int(self.MaxPods / 2) + 1
                DM_quotas = self.MaxPods - UM_quotas
            else:
                UM_quotas = int(self.MaxPods / 2) - 1
                DM_quotas = self.MaxPods - UM_quotas
        else:
            UM_quotas, DM_quotas = int(self.MaxPods / 2), int(self.MaxPods / 2)

        result: Dict[str, List[int, int]] = {}
        for i in self.Nodes:
            result[i] = [0, 0]
        print(self.UM, self.DM)
        print(UM_quotas, DM_quotas)
        for i in self.Nodes:
            print(self.UM, self.DM)
            if self.UM >= UM_quotas and self.DM >= DM_quotas:
                result[i] = [UM_quotas, DM_quotas]
                self.UM -= UM_quotas
                self.DM -= DM_quotas
            elif self.UM >= UM_quotas and self.DM < DM_quotas:
                if self.UM >= self.MaxPods - self.DM:
                    result[i] = [self.MaxPods - self.DM, self.DM]
                    self.UM -= (self.MaxPods - self.DM)
                    self.DM -= self.DM
                else:
                    result[i] = [self.UM, self.DM]
                    self.UM, self.DM = 0, 0
            elif self.UM < UM_quotas and self.DM >= DM_quotas:
                if self.DM >= self.MaxPods - self.UM:
                    result[i] = [self.UM, self.MaxPods - self.UM]
                    self.UM -= self.DM
                    self.DM -= (self.MaxPods - self.UM)
                else:
                    result[i] = [self.UM, self.DM]
                    self.UM, self.DM = 0, 0
            elif self.UM < UM_quotas and self.DM < DM_quotas:
                result[i] = [self.UM, self.DM]
                self.UM, self.DM = 0, 0
            # print(result)
            if self.UM == 0 and self.DM == 0:
                return result

    def Localize(self):
        result = self.get_result()
        print(result)
        generate('./Scheduler/wrk-nginx.yaml', './Scheduler/yaml_file/', result, self.UD[0], self.UD[1], self.machines)
        os.system('kubectl apply -f ./Scheduler/yaml_file/')


class our:
    def __init__(self, maxPods: int, machine: int, U: int, D: int):
         
Pod数量、最大机器数量、U、D 
        self.MaxPods = maxPods
        self.machines = machine
        self.UM = U
        self.DM = D
        self.UD = (U, D)
        self.Nodes = ['skv-node2', 'skv-node3', 'skv-node4', 'skv-node6', 'skv-node7']
        self.NodeRatio: Dict[str, List[float]] = {}
        random.shuffle(self.Nodes)
        self.Nodes = self.Nodes[:machine]

    def get_result(self) -> Dict[str, List[int]]:
        result: Dict[str, List[int]] = {}
        for i in self.Nodes:
            result[i] = [0, 0]
        UM_quotas, DM_quotas = 0, 0

        need = self.UM / self.DM
        record = []
        for i in range(1, self.MaxPods + 1):
            for j in range(1, self.MaxPods + 1):
                if i + j > self.MaxPods:
                    record.append(1)
                else:
                    record.append(abs(i / j - need))

        UM_quotas = int(record.index(min(record)) / self.MaxPods) + 1
        DM_quotas = int(record.index(min(record)) % self.MaxPods) + 1
        print(UM_quotas, DM_quotas)
        i = 0
        while self.UM != 0 or self.DM != 0:
            # print(i, self.UM, self.DM)
            i = i % len(self.Nodes)
            if self.UM >= UM_quotas and self.DM >= DM_quotas:
                result[self.Nodes[i]][0] += UM_quotas
                result[self.Nodes[i]][1] += DM_quotas
                self.UM -= UM_quotas
                self.DM -= DM_quotas
            elif self.UM < UM_quotas and self.DM >= DM_quotas:
                result[self.Nodes[i]][0] += self.UM
                result[self.Nodes[i]][1] += DM_quotas
                self.UM = 0
                self.DM -= DM_quotas
            elif self.UM >= UM_quotas and self.DM < DM_quotas:
                result[self.Nodes[i]][0] += UM_quotas
                result[self.Nodes[i]][1] += self.DM
                self.UM -= UM_quotas
                self.DM = 0
            elif self.UM < UM_quotas and self.DM < DM_quotas:
                result[self.Nodes[i]][0] += self.UM
                result[self.Nodes[i]][1] += self.DM
                self.UM, self.DM = 0, 0
            i += 1
        return result

    def Localize(self):
        result = self.get_result()
        # print(result)
        # print('1111',self.UD)
        generate('./Scheduler/wrk-nginx.yaml', './Scheduler/yaml_file/', result, self.UD[0], self.UD[1], self.machines)
        os.system('kubectl apply -f ./Scheduler/yaml_file/')

    def TrafficAllocation(self):
        TA = TrafficAllocate()
        TA.ExecuteNode()

