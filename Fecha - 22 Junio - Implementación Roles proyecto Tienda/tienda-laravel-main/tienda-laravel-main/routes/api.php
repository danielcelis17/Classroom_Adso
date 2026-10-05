<?php

use App\Http\Controllers\api\AuthController;
use App\Http\Controllers\api\ClienteController;
use App\Http\Controllers\api\FacturaController;
use App\Http\Controllers\api\ProductoController;
use Illuminate\Support\Facades\Route;

Route::post('/login', [AuthController::class, 'login']);

Route::middleware(['auth:sanctum'])->group(function () {
    
    // Rutas accesibles por Admin y Cliente
    Route::middleware(['role:admin,cliente'])->group(function () {
        // Clientes
        Route::get('/clientes/{id}', [ClienteController::class, 'show']);
        Route::put('/clientes/{id}', [ClienteController::class, 'update']);

        // Productos
        Route::get('/productos', [ProductoController::class, 'index']);
        Route::get('/productos/{id}', [ProductoController::class, 'show']);

        // Facturas
        Route::get('/facturas', [FacturaController::class, 'index']);
        Route::get('/facturas/{id}', [FacturaController::class, 'show']);
        Route::post('/facturas', [FacturaController::class, 'store']);
    });

    // Rutas exclusivas del Admin
    Route::middleware(['role:admin'])->group(function () {
        // CRUD de Clientes exclusivo de admin
        Route::get('/clientes', [ClienteController::class, 'index']);
        Route::post('/clientes', [ClienteController::class, 'store']);
        Route::delete('/clientes/{id}', [ClienteController::class, 'destroy']);

        // CRUD de Productos exclusivo de admin
        Route::post('/productos', [ProductoController::class, 'store']);
        Route::put('/productos/{id}', [ProductoController::class, 'update']);
        Route::delete('/productos/{id}', [ProductoController::class, 'destroy']);
    });
});
