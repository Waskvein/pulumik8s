import pulumi_kubernetes as kubernetes
import yaml
from dataclasses import dataclass


def yamlconfig():
    with open('config.yaml') as y:
        config = yaml.safe_load(y)
    return config


@dataclass
class DeploymentArgs:
    name: str = "app"
    image: str = "core.harbor.k8s.devim.team/library/app-master"
    replicas: int = 1
    namespace: str = "apps"


class Appconfig:
    def appname(self):
        with open('config.yaml') as y:
            config = yaml.safe_load(y)
            appname = str(config['name'])
        return appname

    def applabel(self):
        with open('config.yaml') as y:
            config = yaml.safe_load(y)
            label = {"app": str(config['name'])}
        return label

    def repliccacount(self):
        with open('config.yaml') as y:
            config = yaml.safe_load(y)
            repl = int(config['deployment']['replicas'])
        return repl

    def serviceenable(self):
        config = yamlconfig()
        servenabl = str(config['service']['enabled'])
        return servenabl

    def ingressenable(self):
        config = yamlconfig()
        ingenabl = str(config['ingress']['enabled'])
        return ingenabl


class Appcontainer:
    def containerports(self):
        with open('config.yaml') as y:
            config = yaml.safe_load(y)
            c_ports = (config['deployment']['container']['ports'])
            cports = []
            for port in c_ports:
                cports.append(kubernetes.core.v1.ContainerPortArgs(name=str(port['name']),
                                                                   container_port=int(port['containerPort'])))
        return cports

    def containerresources(self):
        config = yamlconfig()
        resources = (config['deployment']['container']['resources'])
        cpulim = str(resources['cpu']['limits'])
        memlim = str(resources['memory']['limits'])
        cpureq = str(resources['cpu']['requests'])
        memreq = str(resources['memory']['requests'])
        lim = {'cpu': cpulim, 'memory': memlim}
        req = {'cpu': cpureq, 'memory': memreq}
        res = kubernetes.core.v1.ResourceRequirementsArgs(limits=lim, requests=req)
        return res

    def imagename(self):
        with open('config.yaml') as y:
            config = yaml.safe_load(y)
            imgname = str(config['deployment']['container']['image'])
        return imgname


class Appservice:
    def serviceports(self):
        with open('config.yaml') as y:
            config = yaml.safe_load(y)
            s_ports = (config['service']['ports'])
            sports = []
            for port in s_ports:
                sports.append(kubernetes.core.v1.ServicePortArgs(name=str(port['name']),
                                                                 port=int(port['port']),
                                                                 target_port=int(port['targetPort']),
                                                                 protocol=str(port['protocol'])))
            return sports


class Appingress:
    def ingressann(self):
        with open('config.yaml') as y:
            config = yaml.safe_load(y)
            ingannotations = config['ingress']['annotations']
            return ingannotations

    def ingressspec(self):
        with open('config.yaml') as y:
            config = yaml.safe_load(y)
            ingspec = kubernetes.networking.v1.IngressSpecArgs(
                rules=[kubernetes.networking.v1.IngressRuleArgs(
                    http=kubernetes.networking.v1.HTTPIngressRuleValueArgs(
                        paths=[kubernetes.networking.v1.HTTPIngressPathArgs(
                            backend=kubernetes.networking.v1.IngressBackendArgs(
                                service=kubernetes.networking.v1.IngressServiceBackendArgs(
                                    name=str(config['name']),
                                    port=kubernetes.networking.v1.ServiceBackendPortArgs(
                                        number=int(config['ingress']['port']),
                                    ),
                                ),
                            ),
                            path=str(config['ingress']['path']),
                            path_type="Prefix",
                        )],
                    ),
                ), kubernetes.networking.v1.IngressRuleArgs(host=str(config['ingress']['hostname']))],
            )
        return ingspec
