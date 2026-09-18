<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

class ImageProcessingController extends Controller
{
    /**
     * Proxy the processing request to the Python microservice.
     */
    public function process(Request $request)
    {
        // Add a long timeout since some image processing takes time
        $response = Http::timeout(60)
            ->post('http://127.0.0.1:5001/api/process', $request->json()->all());

        return response()->json($response->json(), $response->status());
    }

    /**
     * Check if the Python engine is healthy.
     */
    public function health()
    {
        try {
            $response = Http::timeout(5)->get('http://127.0.0.1:5001/api/health');
            return response()->json($response->json(), $response->status());
        } catch (\Exception $e) {
            return response()->json([
                'status' => 'error',
                'message' => 'Python Engine is unreachable.',
                'error' => $e->getMessage()
            ], 503);
        }
    }
}

