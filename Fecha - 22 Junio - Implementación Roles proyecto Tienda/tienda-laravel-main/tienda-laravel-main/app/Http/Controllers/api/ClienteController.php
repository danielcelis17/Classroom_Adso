<?php

namespace App\Http\Controllers\api;

use App\Http\Controllers\Controller;
use App\Models\Cliente;
use Illuminate\Http\Request;

class ClienteController extends Controller
{
    public function index()
    {
        return response()->json(Cliente::all());
    }

    public function show(Request $request, $id)
    {
        $user = $request->user();

        if ($user->isCliente() && $user->cliente_id != $id) {
            return response()->json(['message' => 'Solo puede ver sus propios datos.'], 403);
        }

        $cliente = Cliente::findOrFail($id);
        return response()->json($cliente);
    }

    public function store(Request $request)
    {
        $validated = $request->validate([
            'nombre' => 'required|string',
            'cedula' => 'required|unique:clientes',
            'telefono' => 'nullable|string',
            'email' => 'required|email|unique:clientes',
        ]);

        $cliente = Cliente::create($validated);
        return response()->json($cliente, 201);
    }

    public function update(Request $request, $id)
    {
        $user = $request->user();

        if ($user->isCliente() && $user->cliente_id != $id) {
            return response()->json(['message' => 'Solo puede editar sus propios datos.'], 403);
        }

        $cliente = Cliente::findOrFail($id);
        $cliente->update($request->all());

        return response()->json($cliente);
    }

    public function destroy($id)
    {
        Cliente::destroy($id);
        return response()->json(['message' => 'Cliente eliminado correctamente.']);
    }
}