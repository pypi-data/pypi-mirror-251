# ==================================================================================================================== #
#             _____           _ _               ____  _       _    __                                                  #
#  _ __  _   |_   _|__   ___ | (_)_ __   __ _  |  _ \| | __ _| |_ / _| ___  _ __ _ __ ___                              #
# | '_ \| | | || |/ _ \ / _ \| | | '_ \ / _` | | |_) | |/ _` | __| |_ / _ \| '__| '_ ` _ \                             #
# | |_) | |_| || | (_) | (_) | | | | | | (_| |_|  __/| | (_| | |_|  _| (_) | |  | | | | | |                            #
# | .__/ \__, ||_|\___/ \___/|_|_|_| |_|\__, (_)_|   |_|\__,_|\__|_|  \___/|_|  |_| |_| |_|                            #
# |_|    |___/                          |___/                                                                          #
# ==================================================================================================================== #
# Authors:                                                                                                             #
#   Patrick Lehmann                                                                                                    #
#                                                                                                                      #
# License:                                                                                                             #
# ==================================================================================================================== #
# Copyright 2017-2024 Patrick Lehmann - Bötzingen, Germany                                                             #
#                                                                                                                      #
# Licensed under the Apache License, Version 2.0 (the "License");                                                      #
# you may not use this file except in compliance with the License.                                                     #
# You may obtain a copy of the License at                                                                              #
#                                                                                                                      #
#   http://www.apache.org/licenses/LICENSE-2.0                                                                         #
#                                                                                                                      #
# Unless required by applicable law or agreed to in writing, software                                                  #
# distributed under the License is distributed on an "AS IS" BASIS,                                                    #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.                                             #
# See the License for the specific language governing permissions and                                                  #
# limitations under the License.                                                                                       #
#                                                                                                                      #
# SPDX-License-Identifier: Apache-2.0                                                                                  #
# ==================================================================================================================== #
#
"""
Common platform information gathered from various sources.

.. hint:: See :ref:`high-level help <COMMON/Platform>` for explanations and usage examples.
"""
from enum                  import Flag, auto

from pyTooling.Decorators  import export, readonly
from pyTooling.MetaClasses import ExtendedType
from pyTooling.Versioning  import SemanticVersion


@export
class PythonImplementation(Flag):
	Unknown = 0

	CPython = 1
	PyPy = 2


@export
class PythonVersion(SemanticVersion):
	def __init__(self) -> None:
		from sys import version_info

		super().__init__(version_info.major, version_info.minor, version_info.micro)

	def __eq__(self, other):
		parts = other.split(".")
		for a, b in zip(parts, (self._major, self._minor, self._patch)):
			if int(a) != b:
				return False

		return True


@export
class Platforms(Flag):
	Unknown = 0

	OS_BSD =     auto()        #: Operating System: BSD (Unix).
	OS_Linux =   auto()        #: Operating System: Linux.
	OS_MacOS =   auto()        #: Operating System: macOS.
	OS_Windows = auto()        #: Operating System: Windows.

	OperatingSystem = OS_BSD | OS_Linux | OS_MacOS | OS_Windows  #: Mask: Any operating system.

	SEP_WindowsPath =  auto()  #: Seperator: Path element seperator (e.g. for directories).
	SEP_WindowsValue = auto()  #: Seperator: Value seperator in variables (e.g. for paths in PATH).

	ENV_Native = auto()        #: Environment: :term:`native`.
	ENV_WSL =    auto()        #: Environment: :term:`Windows System for Linux <WSL>`.
	ENV_MSYS2 =  auto()        #: Environment: :term:`MSYS2`.
	ENV_Cygwin = auto()        #: Environment: :term:`Cygwin`.

	Environment = ENV_Native | ENV_WSL | ENV_MSYS2 | ENV_Cygwin  #: Mask: Any environment.

	ARCH_x86_32 =  auto()      #: Architecture: x86-32 (IA32).
	ARCH_x86_64 =  auto()      #: Architecture: x86-64 (AMD64).
	ARCH_AArch64 = auto()      #: Architecture: AArch64.

	Arch_x86 =     ARCH_x86_32 | ARCH_x86_64  #: Mask: Any x86 architecture.
	Arch_Arm =     ARCH_AArch64               #: Mask: Any Arm architecture.
	Architecture = Arch_x86 | Arch_Arm        #: Mask: Any architecture.

	FreeBSD = OS_BSD     | ENV_Native | ARCH_x86_64                                       #: Group: native FreeBSD on x86-64.
	Linux =   OS_Linux   | ENV_Native | ARCH_x86_64                                       #: Group: native Linux on x86-64.
	MacOS =   OS_MacOS   | ENV_Native | ARCH_x86_64                                       #: Group: native macOS on x86-64.
	Windows = OS_Windows | ENV_Native | ARCH_x86_64 | SEP_WindowsPath | SEP_WindowsValue  #: Group: native Windows on x86-64.

	MSYS =    auto()     #: MSYS2 Runtime: MSYS.
	MinGW32 = auto()     #: MSYS2 Runtime: :term:`MinGW32 <MinGW>`.
	MinGW64 = auto()     #: MSYS2 Runtime: :term:`MinGW64 <MinGW>`.
	UCRT64 =  auto()     #: MSYS2 Runtime: :term:`UCRT64 <UCRT>`.
	Clang32 = auto()     #: MSYS2 Runtime: Clang32.
	Clang64 = auto()     #: MSYS2 Runtime: Clang64.

	MSYS2_Runtime = MSYS | MinGW32 | MinGW64 | UCRT64 | Clang32 | Clang64    #: Mask: Any MSYS2 runtime environment.

	Windows_MSYS2_MSYS =    OS_Windows | ENV_MSYS2 | ARCH_x86_64 | MSYS      #: Group: MSYS runtime running on Windows x86-64
	Windows_MSYS2_MinGW32 = OS_Windows | ENV_MSYS2 | ARCH_x86_64 | MinGW32   #: Group: MinGW32 runtime running on Windows x86-64
	Windows_MSYS2_MinGW64 = OS_Windows | ENV_MSYS2 | ARCH_x86_64 | MinGW64   #: Group: MinGW64 runtime running on Windows x86-64
	Windows_MSYS2_UCRT64 =  OS_Windows | ENV_MSYS2 | ARCH_x86_64 | UCRT64    #: Group: UCRT64 runtime running on Windows x86-64
	Windows_MSYS2_Clang32 = OS_Windows | ENV_MSYS2 | ARCH_x86_64 | Clang32   #: Group: Clang32 runtime running on Windows x86-64
	Windows_MSYS2_Clang64 = OS_Windows | ENV_MSYS2 | ARCH_x86_64 | Clang64   #: Group: Clang64 runtime running on Windows x86-64

	Windows_Cygwin32 =      OS_Windows | ENV_Cygwin | ARCH_x86_32            #: Group: 32-bit Cygwin runtime on Windows x86-64
	Windows_Cygwin64 =      OS_Windows | ENV_Cygwin | ARCH_x86_64            #: Group: 64-bit Cygwin runtime on Windows x86-64


@export
class Platform(metaclass=ExtendedType, singleton=True, slots=True):
	"""An instance of this class contains all gathered information available from various sources.

	.. seealso::

	   StackOverflow question: `Python: What OS am I running on? <https://stackoverflow.com/a/54837707/3719459>`__
	"""

	_platform:             Platforms
	_pythonImplementation: PythonImplementation
	_pythonVersion:        PythonVersion

	def __init__(self) -> None:
		import sys
		import os
		import platform
		import sysconfig

		# Discover the Python implementation
		pythonImplementation = platform.python_implementation()
		if pythonImplementation == "CPython":
			self._pythonImplementation = PythonImplementation.CPython
		elif pythonImplementation == "PyPy":
			self._pythonImplementation = PythonImplementation.PyPy
		else:  # pragma: no cover
			self._pythonImplementation = PythonImplementation.Unknown

		# Discover the Python version
		self._pythonVersion = PythonVersion()

		# Discover the platform
		self._platform = Platforms.Unknown

		# system = platform.system()
		machine = platform.machine()
		# architecture = platform.architecture()
		sys_platform = sys.platform
		sysconfig_platform = sysconfig.get_platform()

		# print()
		# print(os.name)
		# print(system)
		# print(machine)
		# print(architecture)
		# print(sys_platform)
		# print(sysconfig_platform)

		if os.name == "nt":
			self._platform |= Platforms.OS_Windows

			if sysconfig_platform == "win32":
				self._platform |= Platforms.ENV_Native | Platforms.ARCH_x86_32 | Platforms.SEP_WindowsPath | Platforms.SEP_WindowsValue
			elif sysconfig_platform == "win-amd64":
				self._platform |= Platforms.ENV_Native | Platforms.ARCH_x86_64 | Platforms.SEP_WindowsPath | Platforms.SEP_WindowsValue
			elif sysconfig_platform.startswith("mingw"):
				if machine == "AMD64":
					self._platform |= Platforms.ARCH_x86_64
				else:  # pragma: no cover
					raise Exception(f"Unknown architecture '{machine}' for Windows.")

				if sysconfig_platform == "mingw_i686":
					self._platform |= Platforms.ENV_MSYS2 | Platforms.MinGW32
				elif sysconfig_platform == "mingw_x86_64":
					self._platform |= Platforms.ENV_MSYS2 | Platforms.MinGW64
				elif sysconfig_platform == "mingw_x86_64_ucrt":
					self._platform |= Platforms.ENV_MSYS2 | Platforms.UCRT64
				elif sysconfig_platform == "mingw_x86_64_clang":
					self._platform |= Platforms.ENV_MSYS2 | Platforms.Clang64
				else:  # pragma: no cover
					raise Exception(f"Unknown MSYS2 architecture '{sysconfig_platform}'.")
			else:  # pragma: no cover
				raise Exception(f"Unknown platform '{sysconfig_platform}' running on Windows.")

		elif os.name == "posix":
			if sys_platform == "linux":
				self._platform |= Platforms.OS_Linux | Platforms.ENV_Native

				if sysconfig_platform == "linux-x86_64":            # native Linux x86_64; Windows 64 + WSL
					self._platform |= Platforms.ARCH_x86_64
				elif sysconfig_platform == "linux-aarch64":         # native Linux Aarch64
					self._platform |= Platforms.ARCH_AArch64
				else:  # pragma: no cover
					raise Exception(f"Unknown architecture '{sysconfig_platform}' for a native Linux.")

			elif sys_platform == "darwin":
				self._platform |= Platforms.OS_MacOS | Platforms.ENV_Native | Platforms.ARCH_x86_64

				# print()
				# print(os.name)
				# print(system)
				# print(machine)
				# print(architecture)
				# print(sys_platform)
				# print(sysconfig_platform)
			elif sys_platform == "msys":
				self._platform |= Platforms.OS_Windows | Platforms.ENV_MSYS2 | Platforms.MSYS

				if machine == "i686":
					self._platform |= Platforms.ARCH_x86_32
				elif machine == "x86_64":
					self._platform |= Platforms.ARCH_x86_64
				else:  # pragma: no cover
					raise Exception(f"Unknown architecture '{machine}' for MSYS2-MSYS on Windows.")

			elif sys_platform == "cygwin":
				self._platform |= Platforms.OS_Windows

				if machine == "i686":
					self._platform |= Platforms.ARCH_x86_32
				elif machine == "x86_64":
					self._platform |= Platforms.ARCH_x86_64
				else:  # pragma: no cover
					raise Exception(f"Unknown architecture '{machine}' for Cygwin on Windows.")

			elif sys_platform.startswith("freebsd"):
				if machine == "amd64":
					self._platform = Platforms.FreeBSD
				else:  # pragma: no cover
					raise Exception(f"Unknown architecture '{machine}' for FreeBSD.")
			else:  # pragma: no cover
				raise Exception(f"Unknown POSIX platform '{sys_platform}'.")
		else:  # pragma: no cover
			raise Exception(f"Unknown operating system '{os.name}'.")

		# print(self._platform)

	@readonly
	def PythonImplementation(self) -> PythonImplementation:
		return self._pythonImplementation

	@readonly
	def IsCPython(self) -> bool:
		"""Returns true, if the Python implementation is a :term:`CPython`.

		:returns: ``True``, if the Python implementation is CPython.
		"""
		return self._pythonImplementation is PythonImplementation.CPython

	@readonly
	def IsPyPy(self) -> bool:
		"""Returns true, if the Python implementation is a :term:`PyPy`.

		:returns: ``True``, if the Python implementation is PyPY.
		"""
		return self._pythonImplementation is PythonImplementation.PyPy

	@readonly
	def PythonVersion(self) -> PythonVersion:
		return self._pythonVersion

	@readonly
	def HostOperatingSystem(self) -> Platforms:
		return self._platform & Platforms.OperatingSystem

	@readonly
	def IsNativePlatform(self) -> bool:
		"""Returns true, if the platform is a :term:`native` platform.

		:returns: ``True``, if the platform is a native platform.
		"""
		return Platforms.ENV_Native in self._platform

	@readonly
	def IsNativeWindows(self) -> bool:
		"""Returns true, if the platform is a :term:`native` Windows x86-64 platform.

		:returns: ``True``, if the platform is a native Windows x86-64 platform.
		"""
		return Platforms.Windows in self._platform

	@readonly
	def IsNativeLinux(self) -> bool:
		"""Returns true, if the platform is a :term:`native` Linux x86-64 platform.

		:returns: ``True``, if the platform is a native Linux x86-64 platform.
		"""
		return Platforms.Linux in self._platform

	@readonly
	def IsNativeMacOS(self) -> bool:
		"""Returns true, if the platform is a :term:`native` macOS x86-64 platform.

		:returns: ``True``, if the platform is a native macOS x86-64 platform.
		"""
		return Platforms.MacOS in self._platform

	@readonly
	def IsMSYS2Environment(self) -> bool:
		"""Returns true, if the platform is a :term:`MSYS2` environment on Windows.

		:returns: ``True``, if the platform is a MSYS2 environment on Windows.
		"""
		return Platforms.ENV_MSYS2 in self._platform

	@readonly
	def IsMSYSOnWindows(self) -> bool:
		"""Returns true, if the platform is a MSYS runtime on Windows.

		:returns: ``True``, if the platform is a MSYS runtime on Windows.
		"""
		return Platforms.Windows_MSYS2_MSYS in self._platform

	@readonly
	def IsMinGW32OnWindows(self) -> bool:
		"""Returns true, if the platform is a :term:`MinGW32 <MinGW>` runtime on Windows.

		:returns: ``True``, if the platform is a MINGW32 runtime on Windows.
		"""
		return Platforms.Windows_MSYS2_MinGW32 in self._platform

	@readonly
	def IsMinGW64OnWindows(self) -> bool:
		"""Returns true, if the platform is a :term:`MinGW64 <MinGW>` runtime on Windows.

		:returns: ``True``, if the platform is a MINGW64 runtime on Windows.
		"""
		return Platforms.Windows_MSYS2_MinGW64 in self._platform

	@readonly
	def IsUCRT64OnWindows(self) -> bool:
		"""Returns true, if the platform is a :term:`UCRT64 <UCRT>` runtime on Windows.

		:returns: ``True``, if the platform is a UCRT64 runtime on Windows.
		"""
		return Platforms.Windows_MSYS2_UCRT64 in self._platform

	@readonly
	def IsClang32OnWindows(self) -> bool:
		"""Returns true, if the platform is a Clang32 runtime on Windows.

		:returns: ``True``, if the platform is a Clang32 runtime on Windows.
		"""
		return Platforms.Windows_MSYS2_Clang32 in self._platform

	@readonly
	def IsClang64OnWindows(self) -> bool:
		"""Returns true, if the platform is a Clang64 runtime on Windows.

		:returns: ``True``, if the platform is a Clang64 runtime on Windows.
		"""
		return Platforms.Windows_MSYS2_Clang64 in self._platform

	@readonly
	def IsCygwin32OnWindows(self) -> bool:
		"""Returns true, if the platform is a 32-bit Cygwin runtime on Windows.

		:returns: ``True``, if the platform is a 32-bit Cygwin runtime on Windows.
		"""
		return Platforms.Windows_Cygwin32 in self._platform

	@readonly
	def IsCygwin64OnWindows(self) -> bool:
		"""Returns true, if the platform is a 64-bit Cygwin runtime on Windows.

		:returns: ``True``, if the platform is a 64-bit Cygwin runtime on Windows.
		"""
		return Platforms.Windows_Cygwin64 in self._platform

	@readonly
	def IsPOSIX(self) -> bool:
		"""
		Returns true, if the platform is POSIX or POSIX-like.

		:returns: ``True``, if POSIX or POSIX-like.
		"""
		return Platforms.SEP_WindowsPath not in self._platform

	@readonly
	def PathSeperator(self) -> str:
		"""
		Returns the path element separation character (e.g. for directories).

		* POSIX-like: ``/``
		* Windows: ``\\``

		:returns: Path separation character.
		"""
		if Platforms.SEP_WindowsPath in self._platform:
			return "\\"
		else:
			return "/"

	@readonly
	def ValueSeperator(self) -> str:
		"""
		Returns the value separation character (e.g. for paths in PATH).

		* POSIX-like: ``:``
		* Windows: ``;``

		:returns: Value separation character.
		"""
		if Platforms.SEP_WindowsValue in self._platform:
			return ";"
		else:
			return ":"

	@readonly
	def ExecutableExtension(self) -> str:
		"""
		Returns the file extension for an executable.

		* Linux: ``""`` (empty string)
		* macOS: ``""`` (empty string)
		* Windows: ``"exe"``
		"""
		if Platforms.OS_Windows in self._platform:
			return "exe"
		elif Platforms.OS_Linux in self._platform:
			return ""
		elif Platforms.OS_MacOS in self._platform:
			return ""
		else:  # pragma: no cover
			raise Exception(f"Unknown operating system.")

	@readonly
	def SharedLibraryExtension(self) -> str:
		"""
		Returns the file extension for a shared library.

		* Linux: ``"so"``
		* macOS: ``"lib"``
		* Windows: ``"dll"``
		"""
		if Platforms.OS_Windows in self._platform:
			return "dll"
		elif Platforms.OS_Linux in self._platform:
			return "so"
		elif Platforms.OS_MacOS in self._platform:
			return "lib"
		else:  # pragma: no cover
			raise Exception(f"Unknown operating system.")

	def __repr__(self) -> str:
		return str(self._platform)

	def __str__(self) -> str:
		runtime = ""

		if Platforms.OS_MacOS in self._platform:
			platform = "MacOS"
		elif Platforms.OS_Linux in self._platform:
			platform = "Linux"
		elif Platforms.OS_Windows in self._platform:
			platform = "Windows"
		else:
			platform = "plat:dec-err"

		if Platforms.ENV_Native in self._platform:
			environment = ""
		elif Platforms.ENV_WSL in self._platform:
			environment = "+WSL"
		elif Platforms.ENV_MSYS2 in self._platform:
			environment = "+MSYS2"

			if Platforms.MSYS in self._platform:
				runtime = " - MSYS"
			elif Platforms.MinGW32 in self._platform:
				runtime = " - MinGW32"
			elif Platforms.MinGW64 in self._platform:
				runtime = " - MinGW64"
			elif Platforms.UCRT64 in self._platform:
				runtime = " - UCRT64"
			elif Platforms.Clang32 in self._platform:
				runtime = " - Clang32"
			elif Platforms.Clang64 in self._platform:
				runtime = " - Clang64"
			else:
				runtime = "rt:dec-err"

		elif Platforms.ENV_Cygwin in self._platform:
			environment = "+Cygwin"
		else:
			environment = "env:dec-err"

		if Platforms.ARCH_x86_32 in self._platform:
			architecture = "x86-32"
		elif Platforms.ARCH_x86_64 in self._platform:
			architecture = "x86-64"
		elif Platforms.ARCH_AArch64 in self._platform:
			architecture = "amd64"
		else:
			architecture = "arch:dec-err"

		return f"{platform}{environment} ({architecture}){runtime}"
