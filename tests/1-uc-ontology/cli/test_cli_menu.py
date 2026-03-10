"""
Testes de Menu Interativo para OntoTools.

Testa o menu TUI usando mocks para evitar interação real.
"""
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock, call
import io
import sys

from onto_tools.adapters.cli.menu import (
    MenuOption,
    InteractiveMenu,
    build_menu,
    get_project_root,
    action_ontology_load,
    action_ontology_normalize,
    action_ontology_query,
    action_about,
)


class TestMenuOption:
    """Testes da classe MenuOption."""
    
    def test_menu_option_with_action(self):
        """MenuOption com action."""
        action = MagicMock()
        option = MenuOption("1", "Test Label", action=action)
        
        assert option.key == "1"
        assert option.label == "Test Label"
        assert option.action == action
        assert option.submenu is None
    
    def test_menu_option_with_submenu(self):
        """MenuOption com submenu."""
        submenu = InteractiveMenu("Sub", "Description")
        option = MenuOption("2", "Submenu Label", submenu=submenu)
        
        assert option.key == "2"
        assert option.label == "Submenu Label"
        assert option.action is None
        assert option.submenu == submenu


class TestInteractiveMenu:
    """Testes da classe InteractiveMenu."""
    
    def test_menu_creation(self):
        """Menu é criado corretamente."""
        menu = InteractiveMenu("Test Menu", "Test Description")
        
        assert menu.title == "Test Menu"
        assert menu.description == "Test Description"
        assert menu.options == []
        assert menu.parent is None
    
    def test_add_option_with_action(self):
        """Adiciona opção com action."""
        menu = InteractiveMenu("Test", "Desc")
        action = MagicMock()
        
        result = menu.add_option("1", "Option 1", action=action)
        
        assert len(menu.options) == 1
        assert menu.options[0].key == "1"
        assert menu.options[0].label == "Option 1"
        assert result == menu  # Fluent interface
    
    def test_add_option_with_submenu_sets_parent(self):
        """Adicionar submenu configura parent."""
        main_menu = InteractiveMenu("Main", "")
        sub_menu = InteractiveMenu("Sub", "")
        
        main_menu.add_option("1", "Go to sub", submenu=sub_menu)
        
        assert sub_menu.parent == main_menu
    
    def test_display_header(self):
        """Header é exibido corretamente."""
        menu = InteractiveMenu("My Title", "My Description")
        
        with patch('click.echo') as mock_echo:
            menu.display_header()
            
            # Verifica que title está no output
            calls = [str(c) for c in mock_echo.call_args_list]
            assert any('My Title' in str(c) for c in calls)
    
    def test_display_options_shows_all_options(self):
        """Display mostra todas as opções."""
        menu = InteractiveMenu("Test", "")
        menu.add_option("1", "First Option")
        menu.add_option("2", "Second Option")
        
        with patch('click.echo') as mock_echo:
            menu.display_options()
            
            calls = [str(c) for c in mock_echo.call_args_list]
            assert any('First Option' in str(c) for c in calls)
            assert any('Second Option' in str(c) for c in calls)
    
    def test_display_options_shows_back_when_has_parent(self):
        """Mostra 'Voltar' quando tem parent."""
        main = InteractiveMenu("Main", "")
        sub = InteractiveMenu("Sub", "")
        main.add_option("1", "Go Sub", submenu=sub)
        
        with patch('click.echo') as mock_echo:
            sub.display_options()
            
            calls = [str(c) for c in mock_echo.call_args_list]
            assert any('Voltar' in str(c) for c in calls)


class TestBuildMenu:
    """Testes da função build_menu."""
    
    def test_build_menu_returns_interactive_menu(self):
        """build_menu retorna InteractiveMenu."""
        menu = build_menu()
        
        assert isinstance(menu, InteractiveMenu)
    
    def test_main_menu_has_expected_options(self):
        """Menu principal tem opções esperadas."""
        menu = build_menu()
        
        option_keys = [opt.key for opt in menu.options]
        
        assert "1" in option_keys  # Ontology
        assert "2" in option_keys  # Query
        assert "3" in option_keys  # Export
        assert "4" in option_keys  # Comparison
        assert "9" in option_keys  # Utils
    
    def test_ontology_submenu_has_all_ucs(self):
        """Submenu de ontologia tem todos os UCs."""
        menu = build_menu()
        
        # Encontrar submenu de ontology
        ontology_option = next(opt for opt in menu.options if opt.key == "1")
        ontology_menu = ontology_option.submenu
        
        assert ontology_menu is not None
        assert len(ontology_menu.options) >= 7  # UC-101 a UC-108 (menos UC-102)
    
    def test_submenus_have_parent_set(self):
        """Submenus têm parent configurado."""
        menu = build_menu()
        
        for option in menu.options:
            if option.submenu:
                assert option.submenu.parent == menu


class TestGetProjectRoot:
    """Testes da função get_project_root."""
    
    def test_returns_path(self):
        """Retorna um Path."""
        result = get_project_root()
        
        assert isinstance(result, Path)
    
    def test_path_exists(self):
        """Path retornado existe."""
        result = get_project_root()
        
        assert result.exists()
    
    def test_path_contains_expected_files(self):
        """Path contém arquivos esperados do projeto."""
        result = get_project_root()
        
        # Deve ter config/
        assert (result / "config").exists() or (result / "src").exists()


class TestMenuActions:
    """Testes das ações do menu."""
    
    @patch('onto_tools.adapters.cli.menu._get_or_create_facade')
    @patch('click.echo')
    def test_action_about_shows_info(self, mock_echo, mock_facade):
        """action_about exibe informações."""
        action_about()
        
        calls = [str(c) for c in mock_echo.call_args_list]
        assert any('ONTO-TOOLS' in str(c) for c in calls)
        assert any('Versão' in str(c) or 'Version' in str(c) for c in calls)
    
    @patch('onto_tools.adapters.cli.menu._get_or_create_facade')
    @patch('click.echo')
    @patch('click.confirm')
    def test_action_normalize_calls_facade(self, mock_confirm, mock_echo, mock_get_facade):
        """action_ontology_normalize chama facade."""
        mock_facade = MagicMock()
        mock_facade._ontology_graph = MagicMock()
        mock_facade.normalize_ontology.return_value = {
            "status": "success",
            "message": "Normalizado"
        }
        mock_get_facade.return_value = mock_facade
        mock_confirm.return_value = True  # Simular usuário confirmando auto_fix
        
        action_ontology_normalize()
        
        mock_facade.normalize_ontology.assert_called_once()
    
    @patch('onto_tools.adapters.cli.menu._get_or_create_facade')
    @patch('click.echo')
    def test_action_normalize_without_ontology_shows_message(self, mock_echo, mock_get_facade):
        """action_normalize sem ontologia mostra mensagem."""
        mock_facade = MagicMock()
        mock_facade._ontology_graph = None
        mock_get_facade.return_value = mock_facade
        
        action_ontology_normalize()
        
        # Deve ter chamado echo pelo menos uma vez
        assert mock_echo.called
    
    @patch('onto_tools.adapters.cli.menu._get_or_create_facade')
    @patch('click.echo')
    @patch('click.prompt')
    def test_action_query_lists_options(self, mock_prompt, mock_echo, mock_get_facade):
        """action_ontology_query lista opções de consulta."""
        mock_facade = MagicMock()
        mock_facade._ontology_graph = MagicMock()
        mock_facade._ontology_graph.graph = MagicMock()
        mock_get_facade.return_value = mock_facade
        
        # Simular escolha de opção 4 (estatísticas)
        mock_prompt.return_value = 4
        mock_facade._ontology_graph.graph.__len__ = MagicMock(return_value=100)
        mock_facade._ontology_graph.graph.subjects = MagicMock(return_value=iter([]))
        
        action_ontology_query()
        
        calls = [str(c) for c in mock_echo.call_args_list]
        # Deve mostrar opções de consulta
        assert any('Listar Classes' in str(c) or 'Classes' in str(c) for c in calls)


class TestMenuNavigation:
    """Testes de navegação do menu."""
    
    def test_exit_option_key(self):
        """Tecla S é para sair."""
        menu = InteractiveMenu("Test", "")
        
        # Simular input 'S' para sair
        with patch('click.prompt', return_value='S'):
            with patch.object(menu, 'clear_screen'):
                with patch.object(menu, 'display_header'):
                    with patch.object(menu, 'display_options'):
                        with pytest.raises(SystemExit):
                            menu.run()
    
    def test_submenu_has_parent(self):
        """Submenu tem referência ao parent."""
        main = InteractiveMenu("Main", "")
        sub = InteractiveMenu("Sub", "")
        main.add_option("1", "Go Sub", submenu=sub)
        
        assert sub.parent == main


class TestMenuIcons:
    """Testes de ícones do menu."""
    
    def test_submenu_has_folder_icon(self):
        """Submenu tem ícone de pasta."""
        menu = InteractiveMenu("Test", "")
        sub = InteractiveMenu("Sub", "")
        menu.add_option("1", "Submenu", submenu=sub)
        
        with patch('click.echo') as mock_echo:
            menu.display_options()
            
            calls = ''.join([str(c) for c in mock_echo.call_args_list])
            assert '📁' in calls
    
    def test_action_has_lightning_icon(self):
        """Action tem ícone de raio."""
        menu = InteractiveMenu("Test", "")
        menu.add_option("1", "Action", action=lambda: None)
        
        with patch('click.echo') as mock_echo:
            menu.display_options()
            
            calls = ''.join([str(c) for c in mock_echo.call_args_list])
            assert '⚡' in calls
