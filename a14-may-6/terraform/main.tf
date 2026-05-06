terraform {
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.0"
    }
  }
}

provider "kubernetes" {
  config_path    = var.kubeconfig_path
  config_context = "k3d-demo"
}

# El mismo namespace que hemos creado con kubectl apply durante la clase,
# pero ahora gestionado por Terraform: si alguien lo borra, Terraform lo recrea.
resource "kubernetes_namespace" "clase14" {
  metadata {
    name = "clase14"
  }
}
