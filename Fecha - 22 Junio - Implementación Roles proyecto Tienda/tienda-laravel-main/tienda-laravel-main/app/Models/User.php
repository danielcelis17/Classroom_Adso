<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Laravel\Sanctum\HasApiTokens;

class User extends Authenticatable
{
    use HasApiTokens, HasFactory, Notifiable;

    protected $fillable = [
        'name',
        'email',
        'password',
        'role_id',
        'cliente_id',
    ];

    protected $hidden = [
        'password',
        'remember_token',
    ];

    public function role()
    {
        return $this->belongsTo(Role::class);
    }

    public function cliente()
    {
        return $this->belongsTo(Cliente::class);
    }

    public function isAdmin(): bool
    {
        return $this->role && $this->role->nombre === 'admin';
    }

    public function isCliente(): bool
    {
        return $this->role && $this->role->nombre === 'cliente';
    }
}