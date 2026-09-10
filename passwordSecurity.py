#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import secrets
import string
import argparse
import sys
from typing import Tuple

# Librería externa (instalar con: pip install bcrypt)
try:
    import bcrypt
except ImportError:
    print("❌ Error: La librería 'bcrypt' no está instalada.", file=sys.stderr)
    print("   Instálala con: pip install bcrypt", file=sys.stderr)
    sys.exit(1)

DEFAULT_LENGTH = 16
MIN_LENGTH = 8
MAX_LENGTH = 512
DEFAULT_ROUNDS = 12

AMBIGUOUS_CHARS = "il1Lo0O"
PROBLEMATIC_SYMBOLS = "<>&\"'"


def generar_contrasena(longitud: int = DEFAULT_LENGTH,
                       excluir_ambiguos: bool = True,
                       excluir_problematicos: bool = True) -> str:
    """
    Genera una contraseña criptográficamente segura.

    Args:
        longitud: Número de caracteres (entre MIN_LENGTH y MAX_LENGTH).
        excluir_ambiguos: Si es True, elimina 'il1Lo0O' para mejor legibilidad.
        excluir_problematicos: Si es True, elimina '<>&"\' para seguridad en webs.

    Returns:
        La contraseña aleatoria como string.

    Raises:
        ValueError: Si la longitud está fuera del rango permitido.
    """
    if not (MIN_LENGTH <= longitud <= MAX_LENGTH):
        raise ValueError(f"La longitud debe estar entre {MIN_LENGTH} y {MAX_LENGTH}.")

    # Construcción dinámica del alfabeto
    alfabeto = string.ascii_letters + string.digits + string.punctuation

    if excluir_ambiguos:
        alfabeto = ''.join(c for c in alfabeto if c not in AMBIGUOUS_CHARS)

    if excluir_problematicos:
        alfabeto = ''.join(c for c in alfabeto if c not in PROBLEMATIC_SYMBOLS)

    # Usamos SystemRandom().choices (implementado en C) para máxima eficiencia
    rng = secrets.SystemRandom()
    return ''.join(rng.choices(alfabeto, k=longitud))


def fortalecer_contrasena(contrasena: str, rondas: int = DEFAULT_ROUNDS) -> str:
    if not contrasena:
        raise ValueError("La contraseña no puede estar vacía.")
    # bcrypt trunca contraseñas > 72 bytes, por eso lanzamos warning si es muy larga
    if len(contrasena.encode('utf-8')) > 72:
        print("⚠️  Advertencia: bcrypt solo usa los primeros 72 bytes.", file=sys.stderr)

    salt = bcrypt.gensalt(rounds=rondas)
    hash_bytes = bcrypt.hashpw(contrasena.encode('utf-8'), salt)
    return hash_bytes.decode('utf-8')


def verificar_contrasena(contrasena: str, hash_almacenado: str) -> bool:
    """Verifica si la contraseña en texto plano coincide con el hash bcrypt."""
    return bcrypt.checkpw(contrasena.encode('utf-8'),
                          hash_almacenado.encode('utf-8'))


def parse_args():
    """Configura y retorna el analizador de argumentos."""
    parser = argparse.ArgumentParser(
        description="Generador y fortalecedor de contraseñas con bcrypt.",
        epilog="Ejemplo de verificación: python script.py -v 'miClave' '$2b$12$...'"
    )

    grupo_generacion = parser.add_argument_group('Generación')
    grupo_generacion.add_argument("-g", "--generate", action="store_true",
                                  help="Genera una nueva contraseña aleatoria.")
    grupo_generacion.add_argument("-l", "--length", type=int, default=DEFAULT_LENGTH,
                                  help=f"Longitud (entre {MIN_LENGTH} y {MAX_LENGTH}).")
    grupo_generacion.add_argument("--incluir-ambiguos", action="store_true",
                                  help="Incluye caracteres ambiguos (p.ej. O,0,l,1).")
    grupo_generacion.add_argument("--incluir-problematicos", action="store_true",
                                  help="Incluye símbolos conflictivos (< > & \" ').")

    grupo_hash = parser.add_argument_group('Fortalecimiento')
    grupo_hash.add_argument("-H", "--hash", type=str, metavar="TEXTO",
                            help="Fortalece (hashea) la contraseña proporcionada.")
    grupo_hash.add_argument("-r", "--rounds", type=int, default=DEFAULT_ROUNDS,
                            help=f"Factor de trabajo de bcrypt (por defecto {DEFAULT_ROUNDS}).")

    grupo_verificacion = parser.add_argument_group('Verificación')
    grupo_verificacion.add_argument("-v", "--verify", nargs=2,
                                    metavar=("CONTRASEÑA", "HASH"),
                                    help="Verifica si la contraseña coincide con el hash.")

    return parser.parse_args()


def main():
    args = parse_args()

    if args.generate:
        try:
            pwd = generar_contrasena(
                longitud=args.length,
                excluir_ambiguos=not args.incluir_ambiguos,
                excluir_problematicos=not args.incluir_problematicos
            )
        except ValueError as e:
            print(f"❌ Error: {e}", file=sys.stderr)
            sys.exit(1)

        print(f"🔑 Contraseña generada: {pwd}")
        print("⚠️  Asegúrate de que nadie mire tu pantalla (shoulder-surfing).")
        # Mostramos el hash de esta contraseña para que el usuario lo guarde
        hash_pwd = fortalecer_contrasena(pwd, rondas=args.rounds)
        print(f"🔐 Hash bcrypt (guarda este valor): {hash_pwd}")
        return

    if args.hash:
        if args.rounds < 4 or args.rounds > 31:
            print("❌ El número de rondas debe estar entre 4 y 31.", file=sys.stderr)
            sys.exit(1)
        hash_pwd = fortalecer_contrasena(args.hash, rondas=args.rounds)
        print(f"🔐 Hash bcrypt: {hash_pwd}")
        return

    if args.verify:
        pwd, hash_almacenado = args.verify
        if verificar_contrasena(pwd, hash_almacenado):
            print("✅ ¡Coinciden! La contraseña es válida.")
        else:
            print("❌ No coinciden. Revisa la contraseña o el hash.")
        return

    print("ℹ️  No se especificó ninguna acción. Mostrando ayuda:\n")
    sys.argv.append("-h")  # Truco para reutilizar el parser
    main()  # Llamada recursiva controlada (solo para mostrar ayuda)


if __name__ == "__main__":
    main()
