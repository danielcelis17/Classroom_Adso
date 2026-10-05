<?php

namespace App\Http\Controllers\api;

use App\Http\Controllers\Controller;
use App\Models\Factura;
use Illuminate\Http\Request;

class FacturaController extends Controller
{
    public function index(Request $request)
    {
        $user = $request->user();

        if ($user->isCliente()) {
            $facturas = Factura::where('cliente_id', $user->cliente_id)->with('productos')->get();
        } else {
            $facturas = Factura::with(['cliente', 'productos'])->get();
        }

        return response()->json($facturas);
    }

    public function store(Request $request)
    {
        $user = $request->user();

        $clienteId = $user->isCliente() ? $user->cliente_id : $request->cliente_id;

        if (!$clienteId) {
            return response()->json(['message' => 'El cliente es requerido.'], 400);
        }

        $factura = Factura::create([
            'cliente_id' => $clienteId,
            'fecha' => now(),
            'total' => $request->total ?? 0,
        ]);

        if ($request->has('productos')) {
            foreach ($request->productos as $prod) {
                $factura->productos()->attach($prod['id'], [
                    'cantidad' => $prod['cantidad'],
                    'precio' => $prod['precio']
                ]);
            }
        }

        return response()->json($factura->load('productos'), 201);
    }

    public function show(Request $request, $id)
    {
        $user = $request->user();
        $factura = Factura::with('productos')->findOrFail($id);

        if ($user->isCliente() && $factura->cliente_id != $user->cliente_id) {
            return response()->json(['message' => 'No tiene acceso a esta factura.'], 403);
        }

        return response()->json($factura);
    }
}