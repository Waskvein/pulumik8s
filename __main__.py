"""A Python Pulumi program"""

import pulumi
from pulumi import ResourceOptions
import pulumi_kubernetes as kubernetes
from pulumi_kubernetes import Provider
from pulumi_kubernetes.apps.v1 import Deployment
from pulumi_kubernetes.core.v1 import Service
from pulumi_kubernetes.networking.v1 import Ingress
from appclasses import Appcontainer, Appconfig, Appservice, Appingress


# Instantiate a Kubernetes Provider and specify the render directory.
render_provider = Provider('k8s-yaml-renderer',
    render_yaml_to_directory='yaml')

labels = { 'app': 'nginx' }
config = Appconfig()
containerspec = Appcontainer()
servicespec = Appservice()
ingresspec = Appingress()
deployment = kubernetes.apps.v1.Deployment("deployment", opts=ResourceOptions(provider=render_provider),
    metadata=kubernetes.meta.v1.ObjectMetaArgs(
        labels=config.applabel(),
        name=config.appname()
    ),
    spec=kubernetes.apps.v1.DeploymentSpecArgs(
        replicas=config.repliccacount(),
        selector=kubernetes.meta.v1.LabelSelectorArgs(
            match_labels=config.applabel(),
        ),
        template=kubernetes.core.v1.PodTemplateSpecArgs(
            metadata=kubernetes.meta.v1.ObjectMetaArgs(
                labels=config.applabel(),
            ),
            spec=kubernetes.core.v1.PodSpecArgs(
                containers=[kubernetes.core.v1.ContainerArgs(
                    image=containerspec.imagename(),
                    name=config.appname(),
                    ports=containerspec.containerports(),
                    resources=containerspec.containerresources()
                )]
            ))))
if config.serviceenable() == "True":
    print(config.serviceenable())
    svc = Service('service', metadata=kubernetes.meta.v1.ObjectMetaArgs(
                  name=config.appname(),
                  labels=config.applabel()
                  ),
                  spec=kubernetes.core.v1.ServiceSpecArgs(
                  ports=servicespec.serviceports()),
                  opts=ResourceOptions(provider=render_provider)
                  )

    if config.ingressenable() == "True":
        ing = Ingress("ingress",
            metadata=kubernetes.meta.v1.ObjectMetaArgs(
                name=config.appname(),
                annotations=ingresspec.ingressann()),
              spec=ingresspec.ingressspec(),
              opts=ResourceOptions(provider=render_provider)
    )
