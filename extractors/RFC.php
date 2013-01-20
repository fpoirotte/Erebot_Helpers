<?php
/*
    This file is part of Erebot.

    Erebot is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Erebot is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Erebot.  If not, see <http://www.gnu.org/licenses/>.
*/

$pattern = '/^       ([0-9]{3})    ((?:RPL|ERR)_[A-Z_0-9]+)$/';
foreach (file($_SERVER['argv'][1]) as $line) {
    $line = rtrim($line);
    if (!preg_match($pattern, $line, $matches))
        continue;
    $name   = $matches[2];
    $value  = (int) ltrim($matches[1], '0');
    if (isset($numerics[$name]) && $numerics[$name] != $value)
        throw new Exception("$name is being overriden");
    $numerics[$name] = $value;
}

asort($numerics);
foreach ($numerics as $name => $value) {
    printf("    /// \\copydoc Erebot_Interface_Numerics::%s.\n", $name);
    printf("    const %-29s = %3d;\n\n", $name, $value);
}
die(0);

