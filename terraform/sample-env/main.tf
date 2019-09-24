provider "google" {
  region      = "${var.region}"
  project     = "${var.project_name}"
  credentials = "${file("${var.credentials_file_path}")}"
}

resource "google_compute_instance" "prod-docker" {
  count = 5

  name         = "tf-prod-docker-${count.index}"
  machine_type = "f1-micro"
  zone         = "${var.region_zone}"
  tags         = ["prod-docker-node"]

  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-minimal-1804-lts"
    }
  }

  network_interface {
    network = "default"

    access_config {
      # Ephemeral
    }
  }

  metadata = {
    ssh-keys = "root:${file("${var.public_key_path}")}"
  }

  provisioner "file" {
    source      = "terraform-gcp.json"
    destination = "terraform-gcp.json"

    connection {
      host  = "${self.network_interface.0.access_config.0.nat_ip}"
      type  = "ssh"
      user  = "root"
      agent = true
    }
  }

  provisioner "remote-exec" {
    connection {
      host        = "${self.network_interface.0.access_config.0.nat_ip}"
      type        = "ssh"
      user        = "root"
      agent       = true
      #private_key = file("${var.private_key_path}")
    }

    inline = [
      "curl -sSL https://get.docker.com/ | sh",
      "usermod -aG docker $USER",
      "docker login -u _json_key --password-stdin https://gcr.io < terraform-gcp.json",
      "docker pull ${var.docker_image_name}:${var.docker_image_version}",
      "docker run -d --cap-add=SYS_PTRACE --hostname ss1:${var.docker_image_version} -p 8022:22 -p 8001:8001 -p 8003:8003 -p 8004:8004 -p 8005:8005 ${var.docker_image_name}:${var.docker_image_version}"
    ]
  }

  service_account {
    scopes = ["https://www.googleapis.com/auth/compute.readonly"]
  }
}

resource "google_compute_firewall" "default" {
  name    = "tf-prod-firewall"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["8022", "8001", "8003", "8004", "8005"]
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["prod-docker-node"]
}
