r"""
Link class
"""
#*****************************************************************************
#  Copyright (C) 2014
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************

from sage.groups.free_group import FreeGroupElement
from sage.groups.braid import Braid
from sage.matrix.constructor import matrix
from sage.rings.integer_ring import ZZ
from sage.groups.braid import BraidGroup
from sage.rings.polynomial.polynomial_ring_constructor import PolynomialRing
from sage.rings.finite_rings.integer_mod import Mod
from sage.plot.arrow import arrow2d
from sage.plot.arrow import arrow
from sage.plot.graphics import Graphics
from sage.plot.plot3d.shapes2 import bezier3d
from sage.graphs.digraph import DiGraph
from copy import deepcopy,copy
from sage.rings.polynomial.laurent_polynomial_ring import LaurentPolynomialRing
from sage.rings.integer_ring import IntegerRing
from sage.combinat.permutation import Permutations
from sage.rings.finite_rings.integer_mod_ring import IntegerModRing

class Link:
    r"""
    The base class for Link, taking input in three formats namely Briadword, gauss_code, dt_code, PD_code, oriented_gauss_code
    """
    def __init__(self, input = None, gauss_code = None, dt_code = None, oriented_gauss_code = None, PD_code = None):

        if type(input) == Braid:
            self._braid = input
            self._gauss_code = None
            self._dt_code = None

        elif gauss_code != None:
            self._braid = None
            self._gauss_code = gauss_code
            self._dt_code = None

        elif dt_code != None:
            self._braid = None
            self._gauss_code = None
            self._dt_code = dt_code

        elif oriented_gauss_code != None:
            self._oriented_gauss_code = oriented_gauss_code
            self._PD_code = None

        elif PD_code != None:
            self._PD_code = PD_code
            self._oriented_gauss_code = None

        else:
            raise Exception("Invalid input")

    def braidword(self):
        r"""
        Returns the braidword of the input.

        OUTPUT:
            - Braidword representation of the INPUT

        EXAMPLES::
        """

        if self._braid != None:
            return list(self._braid.Tietze())

        elif self._gauss_code != None:
            return "Not implemented Error"

        elif self._dt_code != None:
            return "Not Implemented Error"

    def braid(self):
        r"""
        Returns the braid

        OUTPUT:
            - Braid representation of the INPUT

        EXAMPLES::
        """
        if self._braid != None:
            return self._braid

        elif self._gauss_code != None:
            return "Not implemented Error"

        elif self._dt_code != None:
            return "Not Implemented Error"

    def oriented_gauss_code(self):
        r"""
        Returns the oriented gauss code of the input. The oriented gauss
        code has two parts
        a. The gauss code
        b. The orientation of each crossing
        The following orientation was taken into consideration for consturction
        of knots:

        From the outgoing of the overcrossing if we move in the clockwise direction
        to reach the outgoing of the undercrossing then we label that crossing as '-'.

        From the outgoing of the overcrossing if we move in the anticlockwise
        direction to reach the outgoingo the undercrossing then we label that crossing
        as '+'.

        One more consideration we take in while constructing the orientation is:
        The order of the orientation is same as the ordering of the crossings in the
        gauss code.

        OUTPUT:
            - Oriented gauss code of the INPUT

        EXAMPLES::
        """
        if self._oriented_gauss_code != None:
            return self._oriented_gauss_code

    def PD_code(self):
        r"""
        Returns the Planar Diagram code of the knot. The Planar Diagram is returned
        in the following format.

        We construct the crossing by starting with the entering component of the
        undercrossing, move in the clockwise direction and then generate the list.
        Suppose if the crossing is given by [a, b, c, d], then we interpret this
        information as
        a is the entering component of the undercrossing
        b, d are the components of the overcrossing
        c is the leaving component of the undercrossing


        OUTPUT:
            - Planar Diagram representation of the INPUT

        EXAMPLES::
        sage: L = link.Link(oriented_gauss_code = [[-1, +2, -3, 4, +5, +1, -2, +6, +7, 3, -4, -7, -6,-5],['-','-','-','-','+','-','+']])
        sage: L.PD_code()
        [[1, 7, 2, 6], [7, 3, 8, 2], [3, 11, 4, 10], [11, 5, 12, 4], [14, 5, 1, 6], [13, 9, 14, 8], [12, 9, 13, 10]]
        sage: L = link.Link(oriented_gauss_code = [[1, -2, 3, -4, 2, -1, 4, -3],['+','+','-','-']])
        sage: L.PD_code()
        [[6, 1, 7, 2], [2, 5, 3, 6], [8, 4, 1, 3], [4, 8, 5, 7]]
        """
        if self._PD_code != None:
            return self._PD_code

        #Whatever is the crossing one should give the sign for that first
        #the order of the sign is as per the ordering of the crossings as in the gauss code
        #so for example if the gauss code is 1 -3 2 -1 3 -2 then the
        #order of the sign of the crossings is sign of crossing 1 then 3 then at 2
        #and so on and so forth.
        elif self._oriented_gauss_code != None:
            #self._oriented_gauss_code = oriented_gauss_code
            gc = self._oriented_gauss_code[0]
            gc_sign = self._oriented_gauss_code[1]
            l = [0 for i in range(len(gc))]
            for i in range(len(gc)):
                k = abs(gc[i])
                if l[2*(k-1)] == 0:
                    l[2*(k-1)] = (i + 1)*(cmp(gc[i],0))
                else:
                    l[2*k-1] = (i + 1)*(cmp(gc[i],0))
            y = [None for i in range(2*len(gc_sign))]
            for i in range(0,2*len(gc_sign),2):
                if l[i] < 0:
                    #y[i] = 'under'
                    #y[i+1] = 'over'
                    y[i] = -1
                    y[i+1] = 1
                elif l[i] > 0:
                    #y[i] = 'over'
                    #y[i+1] = 'under'
                    y[i] = 1
                    y[i+1] = -1
            l1 = [abs(x) for x in l]
            r = []
            p = [[None for i in range(4)] for i in range(len(gc_sign))]
            for i in range(len(gc_sign)):
                if gc_sign[i] == '-':
                    #if y[2*i] == 'under':
                    if y[2*i] == -1:
                        p[i][0] = l1[2*i]
                        p[i][2] = p[i][0] + 1
                        p[i][3] = l1[2*i+1]
                        p[i][1] = p[i][3] + 1
                    #elif y[2*i+1] == 'under':
                    elif y[2*i+1] == -1:
                        p[i][0] = l1[2*i+1]
                        p[i][3] = l1[2*i]
                        p[i][2] = p[i][0] + 1
                        p[i][1] = p[i][3] + 1
                elif gc_sign[i] == '+':
                    #if y[2*i] == 'under':
                    if y[2*i] == -1:
                        p[i][0] = l1[2*i]
                        p[i][2] = p[i][0] + 1
                        p[i][1] = l1[2*i+1]
                        p[i][3] = p[i][1] + 1
                    #elif y[2*i+1] == 'under':
                    elif y[2*i+1] == -1:
                        p[i][0] = l1[2*i+1]
                        p[i][1] = l1[2*i]
                        p[i][2] = p[i][0] + 1
                        p[i][3] = p[i][1] + 1
            for i in range(len(p)):
                for j in range(4):
                    if p[i][j] == max(l1) + 1:
                        p[i][j] = 1
            return p

    def gauss_code(self):
        r"""
        Returns the gauss_code of the input. Gauss code is generated by the
        following procedure:

        a. We randomly number the crossings
        b. We select a point on the knot and start moving along the component
        c. At each crossing we take the number of the crossing, along with
           sign, which is '-' if it is a undercrossing and '+' if it is a
           overcrossing.

        OUTPUT:
            - Gauss code representation of the INPUT

        EXAMPLES::
        """
        if self._gauss_code != None:
            return self._gauss_code

        elif self._braid != None:
            L = self._braid
            B = L.parent()
            l = self.braidword()
            L = Link(B(l)).dt_code()
            gc = Link(dt_code = L).gauss_code()
            self._gauss_code = gc
            return gc

        elif self._dt_code != None:
            dt = self._dt_code
            gauss = []
            y = [None for i in range(2*len(dt))]
            x = [0 for i in range(2*len(dt))]
            for i in range(len(dt)):
                x[2*i] = 2*i + 1
                x[2*i + 1] = dt[i]
            for i in range(len(dt)):
                if x[2*i+1] > 0:
                    #y[2*i+1] = 'under'
                    #y[2*i] = 'over'
                    y[2*i+1] = -1
                    y[2*i] = 1
                elif x[2*i+1] < 0:
                    #y[2*i+1] = 'over'
                    #y[2*i] = 'under'
                    y[2*i+1] = 1
                    y[2*i] = -1
            for i in range(1,len(x)+1):
                for j in range(0,len(x)):
                    if abs(x[j]) == i:
                        #if y[j] == 'under':
                        if y[j] == -1:
                            gauss.append(-(j//2 + 1))
                        #elif y[j] == 'over':
                        elif y[j] == 1:
                            gauss.append(j//2 + 1)
            self._gauss_code = gauss
            return gauss

    def dt_code(self):
        r"""
        Returns the dt_code.DT code is generated by the following way.

        We start moving along the knot, as we encounter the crossings we
        start numbering them, so every crossing has two numbers assigned to
        it once we have traced the entire knot. Now we take the even number
        associated with every knot. The following sign convention is to be
        followed:
        Take the even number with a negative sign if it is an overcrossing
        that we are encountering.

        OUTPUT:
            - DT Code representation of the INPUT

        EXAMPLES::
        """
        if self._dt_code != None:
            return self._dt_code

        elif self._braid != None:
            b = list(self._braid.Tietze())
            N = len(b)
            #b1 = [abs(x) for x in b]
            #b1 = max(b1)
            label = [0 for i in range(2*N)]
            string = 1
            next_label = 1
            type1 = 0
            crossing = 0
            while(next_label <= 2*N):
                string_found = 0
                for i in range(crossing, N):
                    if(abs(b[i]) == string or abs(b[i]) == string - 1):
                        string_found = 1
                        crossing = i
                        break
                if(string_found == 0):
                    for i in range(0,crossing):
                        if(abs(b[i]) == string or abs(b[i]) == string - 1):
                            string_found = 1
                            crossing = i
                            break
                if(label[2*crossing + next_label%2] == 1):
                    raise Exception("Implemented only for knots")
                else:
                    label[2*crossing + next_label%2] =  next_label
                    next_label = next_label + 1
                if(type1 == 0):
                    if(b[crossing] < 0):
                        type1 = 1
                    else:
                        type1 = -1
                else:
                    type1 = -1 * type1
                    if((abs(b[crossing]) == string and b[crossing] * type1 > 0) or (abs(b[crossing]) != string and b[crossing] * type1 < 0)):
                        if(next_label%2 == 1):
                            label[2*crossing] = label[2*crossing] * -1
                if(abs(b[crossing]) == string):
                    string = string + 1
                else:
                    string = string - 1
                crossing = crossing + 1
            code = [0 for i in range(N)]
            for i in range(N):
                for j in range(N):
                    if label[2*j+1] == 2*i+1:
                        code[i] = label[2*j]
                        break
            return code

        elif self._gauss_code != None:
            gc = self._gauss_code
            l = [0 for i in range(len(gc))]
            for i in range(len(gc)):
                k = abs(gc[i])
                if l[2*(k-1)] == 0:
                    l[2*(k-1)] = (i + 1)*(cmp(gc[i],0))
                else:
                    l[2*k-1] = (i + 1)*(cmp(gc[i],0))
            y = [l[i] for i in range(len(l)) if abs(l[i])%2 == 0]
            x = [(-1)*y[i] for i in range(len(y))]
            return x

    def _braidwordcomponents(self):
        r"""
        Returns the disjoint braid components, if any, else returns the braid itself.
        For example consider the braid [-1, 3, 1, 3] this can be viewed as a braid
        with components as [-1, 1] and [3, 3]. There is no common crossing to these
        two (in sense there is a crossing between strand 1 and 2, crossing between
        3 and 4 but no crossing between strand 2 and 3,so these can be viewed as
        independent components in the braid).

        OUTPUT:
            - List containing the components is returned

        EXAMPLES::

            sage: from sage.knots import link
            sage: B = BraidGroup(4)
            sage: L = link.Link(B([-1, 3, 1, 3]))
            sage: L._braidwordcomponents()
            [[-1, 1], [3, 3]]
            sage: B = BraidGroup(8)
            sage: L = link.Link(B([-1, 3, 1, 5, 1, 7, 1, 6]))
            sage: L._braidwordcomponents()
            [[-1, 1, 1, 1], [3], [5, 7, 6]]
            sage: L = link.Link(B([-2, 4, 1, 6, 1, 4]))
            sage: L._braidwordcomponents()
            [[-2, 1, 1], [4, 4], [6]]
        """
        b = self.braid()
        ml = list(b.Tietze())
        if ml == []:
            raise Exception("The braid remains the same with no components")
        else:
            l = list(set([abs(k) for k in ml]))
            missing1 = list(set(range(min(l),max(l)+1)) - set(l))
            if len(missing1) == 0:
                return [ml]
            else:
                missing = sorted(missing1)
                x = [[] for i in range(len(missing) + 1)]
                for i in range(len(missing)):
                    for j in range(len(ml)):
                        if(ml[j] != 0 and abs(ml[j]) < missing[i]):
                            x[i].append(ml[j])
                            ml[j] = 0
                        elif(ml[j] != 0 and abs(ml[j]) > missing[-1]):
                            x[-1].append(ml[j])
                            ml[j] = 0
                y2 = [x for x in x if x != []]
                return y2

    def _braidwordcomponentsvector(self):
        r"""
        The list from the braidwordcomponents is flattened to give out the vector form.

        OUTPUT:
            - Vector containing braidwordcomponents

        EXAMPLES::

            sage: from sage.knots import link
            sage: B = BraidGroup(4)
            sage: L = link.Link(B([-1, 3, 1, 3]))
            sage: L._braidwordcomponentsvector()
            [-1, 1, 3, 3]
            sage: B = BraidGroup(8)
            sage: L = link.Link(B([-1, 3, 1, 5, 1, 7, 1, 6]))
            sage: L._braidwordcomponentsvector()
            [-1, 1, 1, 1, 3, 5, 7, 6]
            sage: L = link.Link(B([-2, 4, 1, 6, 1, 4]))
            sage: L._braidwordcomponentsvector()
            [-2, 1, 1, 4, 4, 6]
        """
        bc = self._braidwordcomponents()
        return [x for y in bc for x in y]

    def homology_generators(self):
        r"""
        Returns the homology generators of the braidword.
        This method uses the braidwordcomponentsvector to generate the homology generators.
        The position of the repeated element w.r.t the braidwordcomponentvector list is
        compiled into a list.

        OUTPUT:
            - The homology generators relating to the braid word representation

        EXAMPLES::

            sage: from sage.knots import link
            sage: B = BraidGroup(4)
            sage: L = link.Link(B([-1, 3, 1, 3]))
            sage: L.homology_generators()
            [1, 0, 3]
            sage: B = BraidGroup(8)
            sage: L = link.Link(B([-1, 3, 1, 5, 1, 7, 1, 6]))
            sage: L.homology_generators()
            [1, 2, 3, 0, 0, 0, 0]
            sage: L = link.Link(B([-2, 4, 1, 6, 1, 4]))
            sage: L.homology_generators()
            [0, 2, 0, 4, 0]
        """
        x4 = self._braidwordcomponentsvector()
        hom_gen = []
        for j in range(len(x4)-1):
            a = abs(x4[j])
            for i in range(j+1, len(x4)):
                if(a == abs(x4[i])):
                    hom_gen.append(i)
                    break
            else:
                hom_gen.append(0)
        return hom_gen

    def Seifert_Matrix(self):
        r"""
        Returns the Seifert Matrix associated with the braidword.
        This is further used to calculate the Alexander Polynomial.

        OUTPUT:
            - Returns the Seifert Matrix of the link.

        EXAMPLES::

            sage: from sage.knots import link
            sage: B = BraidGroup(4)
            sage: L = link.Link(B([-1, 3, 1, 3]))
            sage: L.Seifert_Matrix()
            [ 0  0]
            [ 0 -1]
            sage: B = BraidGroup(8)
            sage: L = link.Link(B([-1, 3, 1, 5, 1, 7, 1, 6]))
            sage: L.Seifert_Matrix()
            [ 0  0  0]
            [ 1 -1  0]
            [ 0  1 -1]
            sage: L = link.Link(B([-2, 4, 1, 6, 1, 4]))
            sage: L.Seifert_Matrix()
            [-1  0]
            [ 0 -1]
        """
        x5 = self._braidwordcomponentsvector()
        h = self.homology_generators()
        hl = len(h)
        A = matrix(ZZ, hl, hl)
        for i in range(hl):
            if h[i] != 0:
                for j in range(i,hl):
                        if i == j:
                            A[i,j] = -cmp((x5[i] + x5[h[i]]),0)
                        elif (h[i] > h[j]):
                            A[i,j] = 0
                            A[j,i] = 0
                        elif (h[i] <  j):
                            A[i,j] = 0
                            A[j,i] = 0
                        elif (h[i] == j):
                            if(x5[j] > 0):
                                A[i,j] = 0
                                A[j,i] = 1
                            else:
                                A[i,j] = -1
                                A[j,i] = 0
                        elif abs(abs(x5[i]) - abs(x5[j])) > 1:
                            A[i,j] =  0
                        elif (abs(x5[i]) - abs(x5[j]) == 1):
                            A[i,j] = 0
                            A[j,i] = -1
                        elif (abs(x5[j])- abs(x5[i]) == 1):
                            A[i,j] = 1
                            A[j,i] = 0
                        else: # for debugging
                            A[i,j] = 2
                            A[j,i] = 2
            else:
                for k in range(hl):
                    A[k,i] = 0
                    A[i,k] = 0
        k = []
        for i in range(hl):
                if h[i] == 0:
                    k.append(i)
        for i in reversed(k):
                A = A.delete_rows([i])
                A = A.delete_columns([i])
        return A


    def link_number(self):
        r"""
        Returns the link number

        OUTPUT:
            - Link number of the link

        EXAMPLES::

            sage: from sage.knots import link
            sage: B = BraidGroup(4)
            sage: L = link.Link(B([-1, 3, 1, 3]))
            sage: L.link_number()
            4
            sage: B = BraidGroup(8)
            sage: L = link.Link(B([-2, 4, 1, 6, 1, 4]))
            sage: L.link_number()
            5
            sage: L = link.Link(B([1, 2, 1, 2]))
            sage: L.link_number()
            1
        """
        p = self.braid().permutation()
        return len(p.to_cycles())

    def is_knot(self):
        r"""
        Returns true if the link is knot.
        Every knot is a link but the converse is not true.

        OUTPUT:
            - True if knot else False

        EXAMPLES::

            sage: from sage.knots import link
            sage: B = BraidGroup(4)
            sage: L = link.Link(B([1,3,1,-3]))
            sage: L.is_knot()
            False
            sage: B = BraidGroup(8)
            sage: L = link.Link(B([1, 2, 3, 4, 5, 6]))
            sage: L.is_knot()
            True
        """
        if self.link_number() == 1:
            return True
        else:
            return False

    def genus(self):
        r"""
        Returns the genus of the link

        OUTPUT:
            - Genus of the Link

        EXAMPLES::

            sage: from sage.knots import link
            sage: B = BraidGroup(4)
            sage: L = link.Link(B([-1, 3, 1, 3]))
            sage: L.genus()
            0
            sage: B = BraidGroup(8)
            sage: L = link.Link(B([-2, 4, 1, 6, 1, 4]))
            sage: L.genus()
            0
            sage: L = link.Link(B([1, 2, 1, 2]))
            sage: L.genus()
            1
        """
        b = self.braidword()
        if b == []:
            return 0
        else:
            B = self.braid().parent()
            x = self._braidwordcomponents()
            q = []
            genus = 0
            s = [Link(B(x[i])).smallest_equivalent() for i in range(len(x))]
            t = [Link(B(s[i])).link_number() for i in range(len(s))]
            for i,j in enumerate(s):
                if j == []:
                    s[i].append(-2)
            for i in range(len(s)):
                q1 = (abs(k)+1 for k in s[i])
                q2 = max(q1)
                q.append(q2)
            g = [((2 - t[i]) + len(x[i]) - q[i])/2 for i in range(len(x))]
            for i in range(len(g)):
                genus = genus + g[i]
            return genus

    def smallest_equivalent(self):
        r"""
        Returns the smallest representation of the braidword. Implying if braid
        strands remain unused then we remove them and rewrite the structure.
        This preserves the underlying structure.

        OUTPUT:
            - Smallest equivalent of the given braid word representation.

        EXAMPLES::

            sage: from sage.knots import link
            sage: B = BraidGroup(5)
            sage: L = link.Link(B([-2, 4, 2, 4]))
            sage: L.smallest_equivalent()
            [-1, 3, 1, 3]
            sage: L = link.Link(B([-1, 1]))
            sage: L.smallest_equivalent()
            []
        """
        b = list(self.braid().Tietze())
        if not b:
            return list(b)
        else:
            b1 = min([abs(k) for k in b])
            for i in range(len(b)):
                if b[i] > 0:
                    b[i] = b[i] - b1 + 1
                else:
                    b[i] = b[i] + b1 - 1
            return b

    def signature(self):
        r"""
        Returns the signature of the link

        OUTPUT:
            - Signature of the Link

        EXAMPLES::

            sage: from sage.knots import link
            sage: B = BraidGroup(4)
            sage: L = link.Link(B([-1, 3, 1, 3]))
            sage: L.signature()
            -1
            sage: B = BraidGroup(8)
            sage: L = link.Link(B([-2, 4, 1, 6, 1, 4]))
            sage: L.signature()
            -2
            sage: L = link.Link(B([1, 2, 1, 2]))
            sage: L.signature()
            -2
        """
        m = 2*(self.Seifert_Matrix() + self.Seifert_Matrix().transpose())
        e = m.eigenvalues()
        sum = 0
        s = []
        for i,j in enumerate(e):
            s.append(cmp(j,0))
            sum = sum + s[i]
        return sum

    def alexander_polynomial(self, var ='t'):
        r"""
        Returns the alexander polynomial of the link

        OUTPUT:
            - Alexander Polynomial of the Link

        EXAMPLES::

            sage: from sage.knots import link
            sage: B = BraidGroup(4)
            sage: L = link.Link(B([-1, 3, 1, 3]))
            sage: L.alexander_polynomial()
            0
            sage: B = BraidGroup(8)
            sage: L = link.Link(B([-2, 4, 1, 6, 1, 4]))
            sage: L.alexander_polynomial()
            t^2 - 2*t + 1
            sage: L = link.Link(B([1, 2, 1, 2]))
            sage: L.alexander_polynomial()
            t^2 - t + 1
        """
        R = PolynomialRing(ZZ, var)
        t = R.gen()
        m2 = self.Seifert_Matrix() - t* (self.Seifert_Matrix().transpose())
        return m2.determinant()

    def knot_determinant(self):
        r"""
        Returns the determinant of the knot

        OUTPUT:
            - Determinant of the Knot

        EXAMPLES::

            sage: from sage.knots import link
            sage: B = BraidGroup(4)
            sage: L = link.Link(B([-1, 2, 1, 2]))
            sage: L.knot_determinant()
            1
            sage: B = BraidGroup(8)
            sage: L = link.Link(B([2, 4, 2, 3, 1, 2]))
            sage: L.knot_determinant()
            3
            sage: L = link.Link(B([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,2,1,2,2,2,2,2,2,2,1,2,1,2,-1,2,-2]))
            sage: L.knot_determinant()
            65
        """
        if self.is_knot() == True:
            a = self.alexander_polynomial()
            return abs(a(-1))
        else:
            return "is defined for a knot"

    def arf_invariant(self):
        r"""
        Returns the arf invariant only if the link is knot

        OUTPUT:
            - Arf invariant of knot

        EXAMPLES::

            sage: from sage.knots import link
            sage: B = BraidGroup(4)
            sage: L = link.Link(B([-1, 2, 1, 2]))
            sage: L.arf_invariant()
            0
            sage: B = BraidGroup(8)
            sage: L = link.Link(B([-2, 3, 1, 2, 1, 4]))
            sage: L.arf_invariant()
            0
            sage: L = link.Link(B([1, 2, 1, 2]))
            sage: L.arf_invariant()
            1
        """
        if self.is_knot() == True:
            a = self.alexander_polynomial()
            if ((Mod(a(-1),8) == 1) or (Mod(a(-1),8) == 7)):
                return 0
            else:
                return 1
        else:
            raise Exception("Arf invariant is defined only for knots")

    #this is the conversion from braid to planar
    def pd_code(self):
        r"""
        Returns the Planar Diagram Code from the braidword of the knot. Currently the
        functionality is restricted to knots.

        OUTPUT:
            - Planar Diagram code of the knot.

        EXAMPLES::

            sage: from sage.knots import link
            sage: B = BraidGroup(8)
            sage: L = link.Link(B([-1, -2, -1, 2]))
            sage: L.pd_code()
            [[1, 5, 2, 4], [2, 8, 3, 7], [5, 9, 6, 8], [3, 6, 4, 7]]
            sage: L = link.Link(B([1, -2, -1, 2]))
            sage: L.pd_code()
            [[4, 1, 5, 2], [2, 8, 3, 7], [5, 9, 6, 8], [3, 6, 4, 7]]
            sage: L = link.Link(B([3, -2, -1]))
            sage: L.pd_code()
            [[4, 3, 5, 4], [2, 6, 3, 5], [1, 7, 2, 6]]
            sage: L = link.Link(B([-3, 2, 1]))
            sage: L.pd_code()
            [[3, 5, 4, 4], [5, 2, 6, 3], [6, 1, 7, 2]]
        """
        b = list(self._braid.Tietze())
        N = len(b)
        label = [0 for i in range(2*N)]
        string = 1
        next_label = 1
        type1 = 0
        crossing = 0
        while(next_label <= 2*N):
            string_found = 0
            for i in range(crossing, N):
                if(abs(b[i]) == string or abs(b[i]) == string - 1):
                    string_found = 1
                    crossing = i
                    break
            if(string_found == 0):
                for i in range(0,crossing):
                    if(abs(b[i]) == string or abs(b[i]) == string - 1):
                        string_found = 1
                        crossing = i
                        break
            if(label[2*crossing + next_label%2] == 1):
                raise Exception("Implemented only for knots")
            else:
                label[2*crossing + next_label%2] =  next_label
                next_label = next_label + 1
                if(type1 == 0):
                    if b[crossing] == -1:
                        type1 = -1
                    if(b[crossing] < 0 and b[crossing] != -1):
                        type1 = 1
                    else:
                        type1 = -1
                else:
                    type1 = -1 * type1
                    if((abs(b[crossing]) == string and b[crossing] * type1 > 0) or (abs(b[crossing]) != string and b[crossing] * type1 < 0)):
                        if(next_label%2 == 1):
                            label[2*crossing] = label[2*crossing] * -1
            if(abs(b[crossing]) == string):
                string = string + 1
            else:
                string = string - 1
            crossing = crossing + 1
        s = [None for i in range(len(label))]
        for i in range(N):
            if cmp(label[2*i],0) == -1:
                #s[2*i] = 'over'
                #s[2*i+1] = 'under'
                s[2*i] = 1
                s[2*i+1] = -1
            if (label[2*i]%2 == 0 and cmp(label[2*i],0) == 1):
                #s[2*i] = 'under'
                #s[2*i+1] = 'over'
                s[2*i] = -1
                s[2*i+1] = 1
            if (label[2*i+1]%2 == 0 and cmp(label[2*i+1],0) == 1):
                #s[2*i+1] = 'under'
                #s[2*i] = 'over'
                s[2*i+1] = -1
                s[2*i] = 1
        pd = [[None for i in range(4)] for i in range(N)]
        for j in range(N):
            #if s[2*j] == 'under':
            if s[2*j] == -1:
                if cmp(b[j],0) == -1:
                    pd[j][0] = abs(label[2*j])
                    pd[j][3] = abs(label[2*j+1])
                    pd[j][2] = pd[j][0] + 1
                    pd[j][1] = pd[j][3] + 1
                elif cmp(b[j],0) == 1:
                    pd[j][0] = abs(label[2*j])
                    pd[j][1] = abs(label[2*j+1])
                    pd[j][2] = pd[j][0] + 1
                    pd[j][3] = pd[j][1] + 1
            #elif s[2*j] == 'over':
            elif s[2*j] == 1:
                if cmp(b[j],0) == -1:
                    pd[j][0] = abs(label[2*j+1])
                    pd[j][2] = pd[j][0] + 1
                    pd[j][3] = abs(label[2*j])
                    pd[j][1] = pd[j][3] + 1
                if cmp(b[j],0) == 1:
                    pd[j][0] = abs(label[2*j+1])
                    pd[j][2] = pd[j][0] + 1
                    pd[j][1] = abs(label[2*j])
                    pd[j][3] = pd[j][1] + 1
        return pd

    def is_alternating(self):
        r"""
        Returns True if the given knot diagram is alternating else returns False.
        Alternating diagram implies every over cross is followed by an under cross
        or the vice-versa.

        We look at the gauss code if the sign is alternating, True is returned else
        the knot is not alternating False is returned.

        OUTPUT:
            - True if the knot diagram is alternating else False

        EXAMPLES::

            sage: from sage.knots import link
            sage: B = BraidGroup(4)
            sage: L = link.Link(B([-1, -1, -1, -1]))
            sage: L.is_alternating()
            False
            sage: L = link.Link(B([1, -2, -1, 2]))
            sage: L.is_alternating()
            False
            sage: L = link.Link(B([-1, 3, 1,3, 2]))
            sage: L.is_alternating()
            False
            sage: L = link.Link(B([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,2,1,2,2,2,2,2,2,2,1,2,1,2,-1,2,-2]))
            sage: L.is_alternating()
            False
            sage: L = link.Link(B([-1,2,-1,2]))
            sage: L.is_alternating()
            True
        """
        if self.is_knot() == True:
            x = self.gauss_code()
            s = [cmp(x[i],0) for i in range(len(x))]
            if s == [(-1)**i+1 for i in range(len(x))] or s == [(-1)**i for i in range(len(x))]:
                return True
            else:
                return False
        else:
            return False

    def knot_diagram(self):
        x = self.PD_code()
        #p = [i for i in range(len(x))]
        p =[[None for i in range(4)] for i in range(len(x))]
        plt = Graphics()
        for i in range(len(x)):
            #print (p[i],p[i] + 1)
            a = x[i][0]
            plt = plt + arrow((i,i,i), (i + 0.4,i,i), legend_color='purple') + arrow((i+0.6,i,i),(i+1,i,i))
            p[i][0] = ((i,i,i)) #((i,i),(i + 0.4, i))
            p[i][2] = ((i+0.6,i,i)) #((i+0.6,i),(i+1,i))
            plt = plt + arrow((i+0.5,i,i-0.5),(i+0.5,i,i-0.1)) + arrow((i+0.5,i,i+0.1),(i+0.5,i,i+0.5))
            p[i][1] = (i+0.5,i,i-0.5) #((i+0.5,i-0.5),(i+0.5,i-0.1))
            p[i][3] = (i+0.5,i,i+0.1) #((i+0.5,i+0.1),(i+0.5,i+0.5))
        #print p
        #plt = plt + arrow2d((0,1),(1,2))
        #plt = plt + arrow((2,1),(3,2))
        q = [x[j][i] for j in range(len(x)) for i in range(4)]
        r = [list(p[j][i]) for j in range(len(p)) for i in range(4)]
        t = []
        print q
        print r
        for i in range(1,len(q)+1):
            for j in range(len(q)):
                if q[j] == i:
                    t.append(j)
                    #plt = plt + bezier_path([[r[j]]])
        print t
        #s = [(-1)*r[t[i]] for i in range(len(t))]
        for i in range(0,len(t),2):
            print r[t[i]], r[t[i+1]]
            path = [[tuple(r[t[i]]),tuple(r[t[i+1]])]]
            b = bezier3d(path, color='green')
            plt = plt + b
            #plt = plt + bezier_path([[(s[i]),(s[i+1])]]).plot3d()
        return plt

    #*****************************************************************************
    # Various methods for the implementation of the Vogel's algorithm
    # start here.The input is the oriented gauss code where in every cross is
    # given a sign for the orientation. The missing information in the last
    # implementation of PD was which part of the over crossing we encounter first.
    # So we took the braid word as the input, now in addition to the gauss code we
    # take the orientation at every crossing and call it the oriented gauss code.
    # Eventually after this algorithmic implementation we would like to work on
    # making the planar diagram code as a standard input.
    #
    #  The crux of the Vogel algorithm is two steps, identify the unoriented
    # Seifert circle and perform a move. The first part deals with identifying
    # the regions and Seifert circles.
    #*****************************************************************************

    #**************************** PART - 1 ***************************************
    def seifert_circles(self):
        r"""
        Returns the seifert circles from the input. Seifert circles are obtained
        by smoothing the crossings in the following way:
        All the crossings are assigned four numbers which form the components of the
        crossings.
        At a crossing the under cross entering component would go to the over cross
        leaving component and the over cross entering component would go to the
        under cross leaving component.
        We start with a component of the crossing and start smoothing as according to
        the above rule until we return to the starting component.

        OUTPUT:
            - Seifert circles of the given knot.

        EXAMPLES::
        sage: from sage.knots import link
        sage: L = link.Link(oriented_gauss_code = [[1, -2, 3, -4, 2, -1, 4, -3],['+','+','-','-']])
        sage: L.seifert_circles()
        [[6, 2], [8, 4], [7, 5, 3, 1]]
        sage: L = link.Link(oriented_gauss_code = [[-1, +2, 3, -4, 5, -6, 7, 8, -2, -5, +6, +1, -8, -3, -4, -7],['-','-','-','-','+','+','-','+']])
        sage: L.seifert_circles()
        [[10, 6, 12, 2], [16, 8, 14, 4], [13, 9, 3, 15, 5, 11, 7, 1]]
        sage: L = link.Link(oriented_gauss_code = [[-1, +2, -3, 4, +5, +1, -2, +6, +7, 3, -4, -7, -6,-5],['-','-','-','-','+','-','+']])
        sage: L.seifert_circles()
        [[13, 9], [12, 10, 4], [8, 14, 6, 2], [7, 3, 11, 5, 1]]
        sage: L = link.Link(PD_code=[[1, 7, 2, 6], [7, 3, 8, 2], [3, 11, 4, 10], [11, 5, 12, 4], [14, 5, 1, 6], [13, 9, 14, 8], [12, 9, 13, 10]])
        sage: L.seifert_circles()
        [[13, 9], [12, 10, 4], [8, 14, 6, 2], [7, 3, 11, 5, 1]]
        """
        y = self.PD_code()
        z = max([a for b in y for a in b])
        x = deepcopy(y)
        s = [[None for i in range(4)] for i in range(len(x))]
        for i in range(len(x)):
            s[i][0] = 'entering'
            s[i][2] = 'leaving'
            if x[i][1] < x[i][3]:
                s[i][1] = 'entering'
                s[i][3] = 'leaving'
            if x[i][1] > x[i][3]:
                s[i][1] = 'leaving'
                s[i][3] = 'entering'''
        x1 = x
        s1 = s
        r = [[[None,None],[None,None]] for i in range(len(x))]
        for i in range(len(x)):
            for j in [1,3]:
                if s[i][j] == 'leaving':
                    r[i][0][0] = x1[i][0]
                    r[i][0][1] = x1[i][j]
                    del x1[i][j]
                    del x1[i][0]
                    del s1[i][j]
                    del s1[i][0]
                    break
        for i in range(len(x)):
            for j in [0,1]:
                if s1[i][0] == "entering":
                    r[i][1][0] = x1[i][0]
                    r[i][1][1] = x1[i][1]
                elif s1[i][0] == "leaving":
                    r[i][1][0] = x1[i][1]
                    r[i][1][1] = x1[i][0]
        r1 = [a for b in r for a in b]
        dic = dict(sorted(r1))
        for i in dic:
            dic[i] = [dic[i]]
        D = DiGraph(dic)
        d = D.all_simple_cycles()
        for i in d:
            del i[0]
        return d

    def regions(self):
        r"""
        Returns the regions from the input.Regions are obtained always turning left at the crossing.
        The smoothing used for obtaining the Seifert circles case was specific but here whenever a
        crossing in encountered a left turn is taken until we reach the starting component.
        The following procedure is followed for the development of regions:
        Start at a component of the crossing and keep turning left as the crossings are encountered
        until the starting component is reached.
        Append a negative sign to the component if it were encountered in the opposite direction to
        the direction it is actually in.

        OUTPUT:
            - Regions of the knot.

        EXAMPLES::
        sage: from sage.knots import link
        sage: L = link.Link(oriented_gauss_code = [[-1, +2, -3, 4, +5, +1, -2, +6, +7, 3, -4, -7, -6,-5],['-','-','-','-','+','-','+']])
        sage: L.regions()
        [[4, -11], [2, -7], [6, -1], [13, 9], [-4, -10, -12], [-8, -2, -6, -14], [10, -3, 8, -13], [14, -5, 12, -9], [7, 3, 11, 5, 1]]
        sage: L = link.Link(oriented_gauss_code = [[1, -2, 3, -4, 2, -1, 4, -3],['+','+','-','-']])
        sage: L.regions()
        [[-2, -6], [8, 4], [5, 3, -8], [2, -5, -7], [1, 7, -4], [6, -1, -3]]
        sage: L = link.Link(oriented_gauss_code = [[-1, +2, 3, -4, 5, -6, 7, 8, -2, -5, +6, +1, -8, -3, -4, -7],['-','-','-','-','+','+','-','+']])
        sage: L.regions()
        [[6, -11], [15, -4], [9, 3, -14], [2, -9, -13], [1, 13, -8], [12, -1, -7], [5, 11, 7, -16], [-3, 10, -5, -15], [-6, -10, -2, -12], [16, 8, 14, 4]]
        """
        y = self.PD_code()
        x = deepcopy(y)
        x1 = deepcopy(x)
        s = [[None for i in range(4)] for i in range(len(x))]
        for i in range(len(x)):
            s[i][0] = 'entering'
            s[i][2] = 'leaving'
            '''if self.oriented_gauss_code[1][i] == '-':
                s[i][1] = 'leaving'
                s[i][3] = 'entering'
            elif self.oriented_gauss_code[1][i] == '+':
                s[i][1] = 'entering'
                s[i][3] = 'leaving'''
            if x[i][1] < x[i][3]:
                s[i][1] = 'entering'
                s[i][3] = 'leaving'
            if x[i][1] > x[i][3]:
                s[i][1] = 'leaving'
                s[i][3] = 'entering'
        ou = [["under","over","under","over"] for i in range(len(x))]
        r = [[[None,None],[None,None]] for i in range(len(x))]
        r1 = [[[None,None],[None,None]] for i in range(len(x))]
        for i in range(len(x)):
            r[i][0][0] = x[i][0]
            r1[i][0][0] = "under"
            for j in range(1,4):
                if s[i][j] == "entering":
                    r[i][0][1] = x[i][j]
                    r1[i][0][1] = ou[i][j]
                    del x[i][j]
                    del ou[i][j]
                    s[i][j] = 0
                    del ou[i][0]
                    s[i][0] = 0
                    del x[i][0]
        for i in range(len(x)):
            r[i][1][0] = x[i][0]
            r[i][1][1] = x[i][1]
            r1[i][1][0] = ou[i][0]
            r1[i][1][1] = ou[i][1]
            del x[i][1]
            del x[i][0]
            del ou[i][1]
            del ou[i][0]
        r = [a for b in r for a in b]
        r1 = [a for b in r1 for a in b]
        r3 = deepcopy(r)
        lc = [[None,None] for i in range(len(x))]
        for i in range(len(x)):
            #if gc_sign[i] == '-':
            if x1[i][1] > x1[i][3]:
                if r1[2*i+1][0] == 'over':
                    lc[i][0] = r[2*i+1][0]
                lc[i][1] = (-1)*r[2*i][0]
            elif x1[i][1] < x1[i][3]:
                if r1[2*i+1][0] == 'under':
                    lc[i][1] = r[2*i+1][0]
                lc[i][0] = (-1)*r[2*i][1]
        r2 = []
        for i in reversed(range(len(x))):
            r2.append(r[2*i])
            del r[2*i]
        entering = r2[::-1]
        left_component_entering = lc
        leaving = r
        r4 = deepcopy(r)
        for i in r4:
            i[0] = (-1)*i[0]
            i[1] = (-1)*i[1]
        lc1 = [[None,None] for i in range(len(x))]
        for i in range(len(x)):
            #if gc_sign[i] == '-':
            if x1[i][1] > x1[i][3]:
                if r1[2*i+1][0] == 'over':
                    lc1[i][0] = r3[2*i+1][1]
                    if r1[2*i][0] == 'over':
                        lc1[i][1] = (-1)*r3[2*i][0]
                    elif r1[2*i][1] == 'over':
                        lc1[i][1] = (-1)*r3[2*i][1]
            #elif gc_sign[i] == '+':
            elif x1[i][1] < x1[i][3]:
                if r1[2*i+1][1] == 'over':
                    lc1[i][0] = r3[2*i+1][1]
                    if r1[2*i][0] == 'under':
                        lc1[i][1] = (-1)*r3[2*i][0]
                    elif r1[2*i][1] == 'under':
                        lc1[i][1] = (-1)*r3[2*i][1]
        left_component_leaving = lc1
        '''
        sage: L.regions([[-1, +2, -3, 1, -2, +3 ],['-','-','-']])
        [[1, 4], [5, 2], [3, 6]]
        [[5, -1], [3, -5], [1, -3]]
        [[5, 2], [3, 6], [1, 4]]
        read as 1 has left component as 5, 4 has left componet as -1, .....
        read as [1,4], [5,2], [3,6] enter the crossing
        read as [5,2], [3,6], [1,4] leave the crossing
        '''
        w = {}
        w1 = {}
        for i in range(len(x)):
            w.update({entering[i][0] : left_component_entering[i][0]})
            w.update({entering[i][1] : left_component_entering[i][1]})
            w1.update({r4[i][0] : left_component_leaving[i][0]})
            w1.update({r4[i][1] : left_component_leaving[i][1]})
        for i in range(1,len(w)+1):
            w[i] = [w[i]]
        for i in range(-len(w),0):
            w1[i] = [w1[i]]
        w2 = dict(w.items() + w1.items())
        d = DiGraph(w2)
        regions = d.all_simple_cycles()
        for i in regions:
            del i[0]
        check = [i for i in range(-len(w), len(w)+1)]
        del check[len(w)]
        regions1 = [a for b in regions for a in b]
        r5 = sorted(regions1)
        if r5 == check:
            return regions
        else:
            raise Exception("Incorrect Input")

    def vogel_move(self):
        r"""
        Returns the Planar Diagram code if there is a vogel's move required, else returns
        "no move required". Whether a move is required or not is decided by the following
        criteria:
        A bad region is one that has two components with the same sign, but that belong
        to different Seifert circles.
        We detect the presence of a bad region and then perform the move. The move is done as follows:
        Perform a Reidemeister move of type 2 by pulling the component with a higher number
        over the component having the lower number. As this is done we have 2 more crossings added to
        the initial system. We renumber everything and return the Planar Diagram Code of the modified
        diagram

        OUTPUT:
            - Planar diagram after the move is performed.

        EXAMPLES::
        sage: from sage.knots import link
        sage: L = link.Link(oriented_gauss_code = [[1, -2, 3, -4, 2, -1, 4, -3],['+','+','-','-']])
        sage: L.vogel_move()
        'No move required'
        sage: L = link.Link(oriented_gauss_code = [[-1, +2, 3, -4, 5, -6, 7, 8, -2, -5, +6, +1, -8, -3, -4, -7],['-','-','-','-','+','+','-','+']])
        sage: L.vogel_move()
        'No move required'
        sage: L = link.Link(oriented_gauss_code = [[-1, +2, -3, 4, +5, +1, -2, +6, +7, 3, -4, -7, -6,-5],['-','-','-','-','+','-','+']])
        sage: L.vogel_move()
        [[1, 9, 2, 8], [9, 3, 10, 2], [5, 13, 6, 12], [13, 7, 14, 6], [18, 7, 1, 8], [17, 11, 18, 10], [14, 11, 15, 12], [16, 4, 17, 3], [15, 4, 16, 5]]
        sage: L = link.Link(PD_code=[[1, 7, 2, 6], [7, 3, 8, 2], [3, 11, 4, 10], [11, 5, 12, 4], [14, 5, 1, 6], [13, 9, 14, 8], [12, 9, 13, 10]])
        sage: L.vogel_move()
        [[1, 9, 2, 8], [9, 3, 10, 2], [5, 13, 6, 12], [13, 7, 14, 6], [18, 7, 1, 8], [17, 11, 18, 10], [14, 11, 15, 12], [16, 4, 17, 3], [15, 4, 16, 5]]
        """
        z = self.PD_code()
        x = deepcopy(z)
        sc = self.seifert_circles()
        regions = self.regions()
        q1 = deepcopy(regions)
        q = [[[],[]] for i in range(len(regions))]
        for i in range(len(regions)):
            for j in range(len(regions[i])):
                if regions[i][j] < 0:
                    q[i][0].append(regions[i][j])
                elif regions[i][j] > 0:
                    q[i][1].append(regions[i][j])
        r = [[] for i in range(len(q))]
        for i in range(len(q)):
            for j in range(len(q[i])):
                r[i].append(None)
                for k in range(len(q[i][j])):
                    if q[i][j][k] < 0:
                        q[i][j][k] = (-1)*q[i][j][k]
        for i in range(len(q)):
            for j in range(len(q[i])):
                for k in sc:
                    if set(q[i][j]).intersection(set(k)) == set(q[i][j]):
                        r[i][j] = None
                        break
                else:
                    r[i][j] = q[i][j]
        for i in reversed(range(len(r))):
            for j in reversed(range(len(r[i]))):
                if r[i][j] == None:
                    del r[i][j]
        #we see whether they belong to the same region if it is so we remove the other.
        for i in reversed(range(len(r))):
            if len(r[i]) > 1:
                del r[i][1]
            if len(r[i]) == 0:
                del r[i]
        # r has the components together
        r = [a for b in r for a in b]
        if r != []:
            r1 = r[0]
            # we sort r1 to get r2 this is in order to computer c
            r2 = sorted(r1)
            # c has the new components after the move has been made
            c = [[None for i in range(3)] for i in range(len(r2))]
            for i in range(len(c)):
                c[i][0] = r2[i] + 2*i
                c[i][1] = c[i][0] + 1
                c[i][2] = c[i][1] + 1
            #now using the above data in c1 compute the PD info at the new crossings
            #we always pull the component numbered higher onto the component numbered lower
            npd = [[None for i in range(4)] for i in range(len(r1))]
            if max(r1) == r1[0]:
                npd[1][0] = c[1][0]
                npd[1][2] = npd[1][0] + 1
                npd[0][0] = npd[1][2]
                npd[0][2] = npd[0][0] + 1
            elif max(r1) == r1[1]:
                npd[1][0] = c[1][0]
                npd[1][2] = npd[1][0] + 1
                npd[0][0] = npd[1][2]
                npd[0][2] = npd[0][0] + 1
            #now we need to decide the over crossings, for this we need to find which crossing has
            #the highest component leaving since that has the new lowest component entering
            #for i in range(len(r)):
            #for i in [0]:
            if max(r1) == r1[1]:
                if max(c[1]) == max(npd[0]):
                    npd[0][1] = c[0][1]
                    npd[0][3] = c[0][0]
                    npd[1][1] = c[0][1]
                    npd[1][3] = c[0][2]
                elif max(c[1]) == max(npd[1]):
                    npd[1][1] = c[0][1]
                    npd[1][3] = c[0][0]
                    npd[0][1] = c[0][1]
                    npd[0][3] = c[0][2]
            elif max(r1) == r1[0]:
                if max(c[1]) == max(npd[0]):
                    npd[0][1] = c[0][0]
                    npd[0][3] = c[0][1]
                    npd[1][1] = c[0][2]
                    npd[1][3] = c[0][1]
                elif max(c[1]) == max(npd[1]):
                    npd[1][1] = c[0][0]
                    npd[1][3] = c[0][1]
                    npd[0][1] = c[0][2]
                    npd[0][3] = c[0][1]
            #here we computer the planar diagram and store it in y with the new components
            #the npd has the PD Code for new crossings, now we need to modify the previous
            #crossings.
            y = [[None for i in range(4)] for i in range(len(x))]
            for i in range(len(r2)):
                if i+1  < len(r2):
                    for j in range(len(x)):
                        for k in range(4):
                            if x[j][k] < r2[0]:
                                y[j][k] = x[j][k]
                            elif x[j][k] > r2[i] and x[j][k] < r2[i+1]:
                                y[j][k] = x[j][k] + 2*(i+1)
                            elif x[j][k] > r2[len(r2)-1]:
                                y[j][k] = x[j][k] + 2*(i+2)
            #the above PD code has only few elements and not all, as we are updating the
            #previous crossings we can use the sign information from the input.
            for i in range(len(x)):
                #if gc_sign[i] == '-':
                if x[i][1] > x[i][3]:
                    if y[i][0] == None:
                        y[i][0] = y[i][2] - 1
                    if y[i][2] == None:
                        y[i][2] = y[i][0] + 1
                    if y[i][3] == None:
                        y[i][3] = y[i][1] - 1
                    if y[i][1] == None:
                        y[i][1] = y[i][3] + 1
                #elif gc_sign[i] == '+':
                elif x[i][1] < x[i][3]:
                    if y[i][0] == None:
                        y[i][0] = y[i][2] - 1
                    if y[i][2] == None:
                        y[i][2] = y[i][0] + 1
                    if y[i][3] == None:
                        y[i][3] = y[i][1] + 1
                    if y[i][1] == None:
                        y[i][1] = y[i][3] - 1
            y = y + npd
            y1 = [a for b in y for a in b]
            for i in range(len(y)):
                for j in range(4):
                    if y[i][j] == 0:
                        y[i][j] = max(y1)
            return y
        else:
            return "No move required"

    def final(self):
        r"""
        Returns the Planar Diagram code, Seifert circles and regions after all the bad regions
        have been removed by performing the vogel's move.

        OUTPUT:
            - Planar Diagram code, Seifert circle, Regions after the bad regions have been
              removed

        EXAMPLES::
        sage: from sage.knots import link
        sage: L = link.Link(oriented_gauss_code = [[1, -2, 3, -4, 2, -1, 4, -3],['+','+','-','-']])
        sage: L.final()
        [[[6, 2], [8, 4], [7, 5, 3, 1]],
        [[-2, -6], [8, 4], [5, 3, -8], [2, -5, -7], [1, 7, -4], [6, -1, -3]],
        [[6, 1, 7, 2], [2, 5, 3, 6], [8, 4, 1, 3], [4, 8, 5, 7]]]
        sage: L = link.Link(oriented_gauss_code = [[-1, +2, 3, -4, 5, -6, 7, 8, -2, -5, +6, +1, -8, -3, -4, -7],['-','-','-','-','+','+','-','+']])
        sage: L.final()
        [[[10, 6, 12, 2], [16, 8, 14, 4], [13, 9, 3, 15, 5, 11, 7, 1]],
        [[6, -11], [15, -4], [9, 3, -14], [2, -9, -13], [1, 13, -8], [12, -1, -7], [5, 11, 7, -16], [-3, 10, -5, -15], [-6, -10, -2, -12], [16, 8, 14, 4]],
        [[1, 13, 2, 12], [9, 3, 10, 2], [14, 4, 15, 3], [4, 16, 5, 15], [10, 5, 11, 6], [6, 11, 7, 12], [16, 8, 1, 7], [13, 8, 14, 9]]]
        sage: L = link.Link(oriented_gauss_code = [[-1, +2, -3, 4, +5, +1, -2, +6, +7, 3, -4, -7, -6,-5],['-','-','-','-','+','-','+']])
        sage: L.final()
        [[[18, 4], [21, 15], [9, 3, 19, 11, 17, 5, 13, 7, 1], [10, 20, 16, 12, 6, 14, 22, 8, 2]],
        [[-15, -21], [6, -13], [2, -9], [8, -1], [18, 4], [-3, 10, -19], [12, -5, -17], [20, 16, -11], [14, 22, -7], [19, 11, 17, -4], [21, -14, -6, -12, -16], [15, -20, -10, -2, -8, -22], [5, 13, 7, 1, 9, 3, -18]],
        [[1, 9, 2, 8], [9, 3, 10, 2], [5, 13, 6, 12], [13, 7, 14, 6], [22, 7, 1, 8], [19, 11, 20, 10], [16, 11, 17, 12], [18, 4, 19, 3], [17, 4, 18, 5], [21, 14, 22, 15], [20, 16, 21, 15]]]
        """
        x = self.PD_code()
        while True:
            link = Link(PD_code = x)
            PD_code_old =  x
            x = link.vogel_move()
            if x == "No move required":
                x = PD_code_old
                break
        L = Link(PD_code = x)
        sc = L.seifert_circles()
        regions = L.regions()
        pd_code = x
        final = [sc, regions, pd_code]
        return final

    #**************************** PART - 2 ***************************************
    def seifert_to_braid(self):
        r"""
        Returns the braidword of the input. We match the outgoing components to the
        incoming components, in doing so we order the crossings and see to which strand
        they belong, thereby developing the braidword

        OUTPUT:
            - Braidword of the INPUT

        EXAMPLES::
        sage: from sage.knots import link
        sage: L = link.Link(oriented_gauss_code = [[1, -2, 3, -4, 2, -1, 4, -3],['+','+','-','-']])
        sage: L.seifert_to_braid()
        [1, -2, 1, -2]
        sage: L = link.Link(oriented_gauss_code = [[-1, +2, -3, 4, +5, +1, -2, +6, +7, 3, -4, -7, -6,-5],['-','-','-','-','+','-','+']])
        sage: L.seifert_to_braid()
        [-1, -2, -3, 2, 1, -2, -2, 3, 2, -2, -2]
        sage: L = link.Link(oriented_gauss_code = [[-1, +2, 3, -4, 5, -6, 7, 8, -2, -5, +6, +1, -8, -3, -4, -7],['-','-','-','-','+','+','-','+']])
        sage: L.seifert_to_braid()
        [-1, 2, -1, -2, -2, 1, 1, -2]
        """
        sc = self.final()[0]
        regions = self.final()[1]
        pd_code = self.final()[2]
        sign = []
        for i in pd_code:
            if i[1] > i[3]:
                sign.append('-')
            elif i[1] < i[3]:
                sign.append('+')
        entering = []
        leaving = []
        for i in range(len(pd_code)):
            t = []
            q = []
            if sign[i] == '-':
                t.append(pd_code[i][0])
                t.append(pd_code[i][3])
                q.append(pd_code[i][1])
                q.append(pd_code[i][2])
            elif sign[i] == '+':
                t.append(pd_code[i][0])
                t.append(pd_code[i][1])
                q.append(pd_code[i][2])
                q.append(pd_code[i][3])
            entering.append(t)
            leaving.append(q)
        #making regions positive
        for i in regions:
            for j in range(len(i)):
                if i[j] < 0:
                    i[j] = (-1)*i[j]
        #finding which sc are same as regions
        #r[0] is the first seifert cirlce and r[1] is the last one
        #which coincides with a region and there are exactly two seifert
        #circles here.
        r = []
        for i in sc:
            for j in regions:
                if set(i) == set(j):
                    r.append(i)
                    break
        #here t stores the crossing information required to check which one
        #is the next
        t = [[None for i in range(2*len(sc[j]))] for j in range(len(sc))]
        for i in range(len(sc)):
            for j in range(len(sc[i])):
                t[i][2*j] = sc[i][j] - 1
                t[i][2*j+1] = sc[i][j] + 1
        #here we find the order of the seifert circles
        e = []
        t1 = deepcopy(t)
        a = r[0]
        b = r[1]
        del t[0]
        i = 0
        while True:
            for i in range(len(t)):
                if len(list(set(a).intersection(set(t[i])))) != 0:
                    r = t1.index(t[i])
                    e.append(a)
                    del t[i]
                    a = sc[r]
                    break
            else:
                e.append(b)
                break
        t = []
        flatentering = [a for b in entering for a in b]
        for i in flatentering:
            for k in e:
                if i in k:
                    t.append(e.index(k))
        for i in range(len(entering)):
            if sign[i] == '-':
                if t[2*i] > t[2*i+1]:
                    a = entering[i][0]
                    entering[i][0] = entering[i][1]
                    entering[i][1] = a
                    b = leaving[i][0]
                    leaving[i][0] = leaving[i][1]
                    leaving[i][1] = b
        bn = {}
        for i in range(len(e)):
            bn.update({i + 1 : e[i]})
        crossingtoseifert = {}
        for i in bn.iterkeys():
            crossingtoseifert.update({i:[]})
        for i in bn.iterkeys():
            for k in pd_code:
                if len(list(set(bn[i]).intersection(set(k)))) == 2:
                    crossingtoseifert[i].append(k)
        crossingtoseifertcp = deepcopy(crossingtoseifert)
        crossingtoseifertsign = {}
        for i in crossingtoseifert.iterkeys():
            crossingtoseifertsign.update({i:[]})
        for i in crossingtoseifert.iterkeys():
            for j in crossingtoseifert[i]:
                if j[1] > j[3]:
                    crossingtoseifertsign[i].append(-1)
                if j[1] < j[3]:
                    crossingtoseifertsign[i].append(1)
        crossingtoseifertsigncp = deepcopy(crossingtoseifertsign)
        tmp = []
        reg = [0 for i in range(len(sc))]
        if crossingtoseifertsign[1][0] == -1:
            tmp.append(crossingtoseifert[1][0][1])
            tmp.append(crossingtoseifert[1][0][2])
        elif crossingtoseifertsign[1][0] == 1:
            tmp.append(crossingtoseifert[1][0][2])
            tmp.append(crossingtoseifert[1][0][3])
        for i,j in enumerate(leaving):
            if set(tmp) == set(j):
                if sign[i] == '-':
                    reg[0] = j[0]
                    reg[1] = j[1]
                elif sign[i] == '+':
                    reg[0] = j[1]
                    reg[1] = j[0]
        crossing = []
        crossing.append(crossingtoseifert[1][0])
        q = 0
        while q < len(pd_code):
            for val in zip(reg, reg[1:]):
                for i in range(len(entering)):
                    if set(val) == set(entering[i]):
                        crossing.append(pd_code[i])
                        if sign[i] == '-':
                            reg[reg.index(val[0])] = leaving[i][0]
                            reg[reg.index(val[1])] = leaving[i][1]
                            q = q + 1
                            break
                        elif sign[i] == '+':
                            if list(val) == entering[i]:
                                reg[reg.index(val[0])] = leaving[i][1]
                                reg[reg.index(val[1])] = leaving[i][0]
                            elif set(val) == set(entering[i]):
                                reg[reg.index(val[0])] = leaving[i][0]
                                reg[reg.index(val[1])] = leaving[i][1]
                            q = q + 1
                            break
                    if len(list(set(val).intersection(set(entering[i])))) == 1 and 0 in set(val):
                        crossing.append(pd_code[i])
                        if sign[i] == '-':
                            reg[reg.index(val[0])+1] = leaving[i][1]
                            reg[reg.index(val[0])] = leaving[i][0]
                            q = q + 1
                            break
                        elif sign[i] == '+':
                            reg[reg.index(val[0])+1] = pd_code[i][2]
                            reg[reg.index(val[0])] = pd_code[i][3]
                            q = q + 1
                            break
        del crossing[len(pd_code)]
        for i in range(1,len(sc)):
            for j in crossingtoseifertcp[i]:
                x = crossingtoseifertcp[i+1].index(j)
                del crossingtoseifertcp[i+1][x]
                del crossingtoseifertsigncp[i+1][x]
        braid = []
        for i in crossing:
            for j,k in crossingtoseifertcp.items():
                for l in k:
                    if i == l:
                        braid.append(j*crossingtoseifertsigncp[j][k.index(l)])
        return braid

    def writhe(self):
        x = self.oriented_gauss_code()
        pos = x[1].count('+')
        neg = (-1)*x[1].count('-')
        return pos + neg

    def jones_polynomial(self, var = 't'):
        r"""
        Returns the jones polynomial of the input. The following procedure is used to
        determine the jones polynomial. We track the trip matrix of the knot and keep
        changing through the various combinations of smoothing the knot.

        OUTPUT:
            - Jones Polynomial of the INPUT

        EXAMPLES::
        sage: from sage.knots import link
        sage: L = link.Link(oriented_gauss_code = [[1, -2, 3, -4, 2, -1, 4, -3],['+','+','-','-']])
        sage: L.jones_polynomial()
        t^8 - t^4 + 1 - t^-4 + t^-8
        sage: L = link.Link(oriented_gauss_code = [[-1, +2, -3, 4, +5, +1, -2, +6, +7, 3, -4, -7, -6,-5],['-','-','-','-','+','-','+']])
        sage: L.jones_polynomial()
        -t^16 + t^12 + t^4
        """
        x = self.oriented_gauss_code()
        crossinfo = deepcopy(x[0])
        signinfo = x[1]
        poscross = [abs(i) for i in x[0]]
        z = []
        for i in range(len(poscross)):
            for j in range(i+1, len(poscross)):
                if poscross[i] == poscross[j]:
                   z.append(poscross[i:j])
        counts = [[] for i in range(len(z))]
        for i in range(len(z)):
            for j in z[i]:
                counts[i].append(Mod(z[i].count(j),2))
        A = matrix(IntegerModRing(2), max(poscross), max(poscross))
        for i in range(len(z)):
            for j in range(len(z[i])):
                A[z[i][j]-1,i] = counts[i][j]
        for i in range(len(poscross)):
            for j in reversed(range(i+1,len(poscross))):
                if poscross[i] == poscross[j]:
                    del poscross[j]
        crosstosign = {}
        for i in range(len(poscross)):
            crosstosign.update({poscross[i] : signinfo[i]})
        firstarray = []
        for i,j in crosstosign.items():
            if j == '-':
                A[i-1,i-1] = 1
                firstarray.append(1)
            elif j == '+':
                A[i-1,i-1] = 0
                firstarray.append(0)
        R = LaurentPolynomialRing(ZZ, var)
        x = R.gen()
        labels1 = [x for i in range(2*len(poscross))]
        labels2 = [x**(-1) for i in range(2*len(poscross))]
        labels1.extend(labels2)
        P = Permutations(labels1, len(poscross))
        perlist = P.list()
        coeff = []
        s = 0
        for i,j in enumerate(perlist):
            Acp = deepcopy(A)
            for k,l in enumerate(j):
                if l == x**(-1):
                    if Acp[k,k] == 0:
                        Acp[k,k] = 1
                    elif Acp[k,k] == 1:
                        Acp[k,k] = 0
            coeff.append((x**j.count(x)) * (x**((-1)*j.count(x**(-1)))) * \
            ((-1)*(x**2 + x**(-2)))**Acp.nullity())
        for i in coeff:
            s = s + i
        wri = self.writhe()
        s = s*(((-1)*(x**(-3)))**wri)
        return s
