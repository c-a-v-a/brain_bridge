{
  description = "Flake for BrainBridge project";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem
      (system:
        let
          pkgs = nixpkgs.legacyPackages.${system};
        in
        {
          devShells.default = pkgs.mkShell {
            buildInputs = with pkgs; [
              bun
              pylint
              (python3.withPackages (python-pkgs: with python-pkgs;[
                fastapi
                pydantic
                uvicorn
              ]))
              vscodium
            ];
          };
        }
      );
}
