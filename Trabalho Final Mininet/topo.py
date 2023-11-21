from mininet.topo import Topo

class MyTopo(Topo):
    """
    MyTopo cria uma topologia de rede customizada, de acordo com a segunda parte do trabalho final de Mininet.
    """

    def __init__(self):
        # Inicializando a topologia
        Topo.__init__(self)

        # Adicionando os Hosts da topologia
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')
        h5 = self.addHost('h5')
        h6 = self.addHost('h6')
        h7 = self.addHost('h7')
        h8 = self.addHost('h8')
        h9 = self.addHost('h9')

        # Adicionando os Switches da topologia
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')

        # Adicionando os links entre as máquinas
        # H1, H2 -> S1
        self.addLink(h1, s1)
        self.addLink(h2, s1)

        # H3, H4 -> S2
        self.addLink(h3, s2)
        self.addLink(h4, s2)

        # H5, H6 -> S3
        self.addLink(h5, s3)
        self.addLink(h6, s3)

        # H7, H8, H9 -> S4
        self.addLink(h7, s4)
        self.addLink(h8, s4)
        self.addLink(h9, s4)

        # Conexão entre os switches
        self.addLink(s1, s2)
        self.addLink(s2, s3)
        self.addLink(s3, s4)

topos = {'mytopo': (lambda: MyTopo())}