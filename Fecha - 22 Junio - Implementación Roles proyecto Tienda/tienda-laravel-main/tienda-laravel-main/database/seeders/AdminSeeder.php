<?php

namespace Database\Seeders;

use App\Models\Role;
use App\Models\User;
use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\Hash;

class AdminSeeder extends Seeder
{
    public function run(): void
    {
        $adminRole = Role::where('nombre', 'admin')->first();

        User::firstOrCreate(
            ['email' => 'admin@tienda.com'],
            [
                'name' => 'Administrador',
                'password' => Hash::make('admin12345'),
                'role_id' => $adminRole->id,
            ]
        );
    }
}