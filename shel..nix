let
  pkgs = import <nixpkgs> {};
in pkgs.mkShell {
  LD_LIBRARY_PATH = "${pkgs.stdenv.cc.cc.lib}/lib";
  nativeBuildInputs = [
    pkgs.poetry
    pkgs.python3
  ];
}