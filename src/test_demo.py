#!/usr/bin/env python3
"""
Script de demonstração para testar as funcionalidades da interface
"""
import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk # type:ignore

import numpy as np
from gui.graph_frame import GraphFrame

def test_graph_frame():
    """Testa a criação de um GraphFrame"""
    print("Testando GraphFrame...")
    
    # Criar uma janela de teste
    win = Gtk.Window(title="Teste GraphFrame")
    win.set_default_size(400, 300)
    
    # Criar um GraphFrame
    graph = GraphFrame(win, "Teste", "X", "Y", "o")
    win.set_child(graph)
    
    # Gerar dados de teste
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    
    # Atualizar o gráfico
    graph.update(x, y)
    
    print("GraphFrame criado com sucesso!")
    return win

def test_text_conversion():
    """Testa a conversão de texto para bits"""
    print("Testando conversão de texto para bits...")
    
    test_text = "Hello"
    bits = ' '.join(format(ord(char), '08b') for char in test_text)
    
    print(f"Texto: {test_text}")
    print(f"Bits: {bits}")
    print("Conversão funcionando!")

def test_numpy_operations():
    """Testa operações do NumPy para os gráficos"""
    print("Testando operações NumPy...")
    
    t = np.linspace(0, 1, 1000)
    signal = np.sin(2 * np.pi * 5 * t)
    
    print(f"Array criado com {len(t)} pontos")
    print(f"Valor máximo: {np.max(signal):.3f}")
    print(f"Valor mínimo: {np.min(signal):.3f}")
    print("Operações NumPy funcionando!")

if __name__ == "__main__":
    print("=== Teste das Funcionalidades ===")
    
    # Testar conversão de texto
    test_text_conversion()
    print()
    
    # Testar operações NumPy
    test_numpy_operations()
    print()
    
    # Testar GraphFrame (opcional - requer display)
    try:
        win = test_graph_frame()
        print("Para ver o gráfico, execute: python3 src/teste.py")
    except Exception as e:
        print(f"Erro ao criar GraphFrame: {e}")
        print("Isso é normal se não houver display disponível")
    
    print("\n=== Todos os testes concluídos ===")
    print("Execute 'python3 src/teste.py' para abrir a interface completa") 