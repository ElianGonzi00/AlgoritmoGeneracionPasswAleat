# 🔐 Password Manager CLI

Script en Python para **generar contraseñas aleatorias criptográficamente seguras** y **fortalecerlas mediante hashing con bcrypt**. Diseñado para uso en línea de comandos, con énfasis en seguridad, eficiencia y portabilidad.

---

## 📌 Descripción

Este proyecto resuelve dos problemas concretos:

1. **Generación de contraseñas seguras**: usa `secrets.SystemRandom()` (entropía del sistema operativo) en lugar de `random`, lo que garantiza imprevisibilidad incluso ante atacantes que conocen el algoritmo.
2. **Fortalecimiento de contraseñas**: aplica `bcrypt` con sal automática y factor de trabajo ajustable, transformando cualquier contraseña en un hash irreversible resistente a ataques de fuerza bruta y tablas arcoíris.

---

## ⚙️ Requisitos

- **Python 3.8** o superior.
- Librería externa: [`bcrypt`](https://pypi.org/project/bcrypt/).

Instalación de dependencias:

```bash
pip install bcrypt
```

---

## 🚀 Instalación

```bash
git clone https://github.com/<tu-usuario>/<tu-repo>.git
cd <tu-repo>
pip install -r requirements.txt
```

Si no tienes `requirements.txt`, créalo con:

```
bcrypt>=4.0.0
```

---

## 🧭 Uso

El script se ejecuta desde la terminal y ofrece tres modos: **generar**, **hashear** y **verificar**.

### 1. Generar una contraseña aleatoria

```bash
python password_manager.py --generate
```

Salida esperada:

```
🔑 Contraseña generada: xT7#mQp$2wR!zK&a
⚠️  Asegúrate de que nadie mire tu pantalla (shoulder-surfing).
🔐 Hash bcrypt (guarda este valor): $2b$12$...
```

### 2. Generar con parámetros personalizados

```bash
python password_manager.py -g --length 24 --incluir-ambiguos --incluir-problematicos
```

### 3. Fortalecer (hashear) una contraseña existente

```bash
python password_manager.py --hash "MiClaveSuperSecreta" --rounds 14
```

Salida esperada:

```
🔐 Hash bcrypt: $2b$14$...
```

### 4. Verificar una contraseña contra su hash

```bash
python password_manager.py --verify "MiClaveSuperSecreta" "$2b$14$..."
```

Salida esperada:

```
✅ ¡Coinciden! La contraseña es válida.
```

---

## 🧩 Opciones disponibles

| Bandera corta | Bandera larga             | Descripción                                                        | Valor por defecto |
| :-----------: | :------------------------ | :----------------------------------------------------------------- | :---------------: |
| `-g`          | `--generate`              | Genera una contraseña aleatoria.                                   | —                 |
| `-l`          | `--length`                | Longitud de la contraseña (entre 8 y 512).                         | `16`              |
| `-H`          | `--hash`                  | Hashea la contraseña proporcionada.                                | —                 |
| `-r`          | `--rounds`                | Factor de trabajo de bcrypt (entre 4 y 31).                        | `12`              |
| `-v`          | `--verify`                | Verifica contraseña contra un hash. Formato: `-v CONTRASEÑA HASH`. | —                 |
| —             | `--incluir-ambiguos`      | Incluye caracteres ambiguos (`i l 1 L o 0 O`).                     | Excluidos         |
| —             | `--incluir-problematicos` | Incluye símbolos conflictivos (`< > & " '`).                       | Excluidos         |

---

## 🔒 Fundamento de seguridad

| Componente                | Implementación                                | Razón                                                                                              |
| :------------------------ | :-------------------------------------------- | :------------------------------------------------------------------------------------------------- |
| **Generación aleatoria**  | `secrets.SystemRandom()`                      | Usa la entropía del kernel (`/dev/urandom` en Linux, `CryptGenRandom` en Windows). No es predecible. |
| **Alfabeto**              | Mayúsculas + minúsculas + dígitos + símbolos  | Maximiza la entropía por carácter.                                                                 |
| **Hashing**               | `bcrypt` con sal de 16 bytes                  | Función *slow-hash* diseñada para contraseñas; resistente a GPU/ASIC.                              |
| **Factor de trabajo**     | Configurable (`--rounds`, por defecto `12`)   | Coste exponencial `2^rounds`. Ajustable según el hardware disponible.                              |
| **Límite de longitud**    | `MAX_LENGTH = 512`                            | Previene ataques de agotamiento de memoria (DoS) por entradas gigantes.                            |
| **Filtros de exclusión**  | Ambiguos y problemáticos desactivados por defecto | Evita errores de transcripción y conflictos en entornos web/shell.                                 |

---

## 📂 Estructura del proyecto

```
.
├── password_manager.py    # Script principal
├── requirements.txt       # Dependencias
└── README.md              # Este archivo
```

---

## ⚠️ Advertencias

- **No almacenes la contraseña en texto plano**. Este script genera el hash, pero es tu responsabilidad guardarlo en una base de datos segura.
- **bcrypt trunca entradas > 72 bytes**. El script advierte si esto ocurre.
- **La contraseña se imprime en pantalla** al generarla. Úsalo en un entorno privado.
- **Aumenta `--rounds`** (a 13 o 14) en servidores modernos para mayor seguridad; el coste es tiempo de cómputo (~0.1–0.5 s por hash).

---

## 🛠️ Roadmap (opcional)

- [ ] Soporte para `argon2-cffi` como alternativa a bcrypt.
- [ ] Exportación del hash a archivo `.json` o `.env`.
- [ ] Pruebas unitarias con `pytest`.
- [ ] Empaquetado como CLI instalable con `pipx`.
