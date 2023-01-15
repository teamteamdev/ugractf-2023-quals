{ pkgs, ... }:

{
  boot.kernelPackages = pkgs.linuxPackages_latest;

  services.nginx = {
    commonHttpConfig = ''
      # For depth
      large_client_header_buffers 4 32k;
    '';

    virtualHosts."ugrac1f.ru" = {
      forceSSL = true;
      enableACME = true;
      locations."/" = {
        root = "/var/lib/staging_tasks/seeker/html";
      };
    };
  };

  virtualisation.docker.enableSysbox = true;
}
