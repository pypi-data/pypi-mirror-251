




module mod_Circuit 
    implicit none 


    type,public::Circuit
        private
        logical::initialized = .False.
        integer*8::Nq 
        integer*8::d 
        complex*16,allocatable::S(:)

        contains
            procedure,pass::Initialization 
            procedure,pass::getState
            procedure,pass::OneQubitGate => U2 
            procedure,pass::TwoQubitGate => U4 
            procedure,pass::runWithGatesFile
            procedure,pass::stdoutMeasurement
    endtype

    private::Initialization
    private::getState
    private::U2,U4 
    private::runWithGatesFile
    private::stdoutMeasurement

    contains

    subroutine Initialization(self,Nq)
        implicit none 
        class(Circuit),intent(inout)::self
        integer*8,intent(in)::Nq 
        ! --------------------------
        if (self%initialized) deallocate(self%S) 
        self%initialized = .True. 
        self%Nq = Nq 
        allocate(self%S(0:2_8**self%Nq-1_8))
        self%S = (0._8,0._8) 
        self%S(0) = (1._8,0._8)
        self%d = 2_8**self%Nq 
    endsubroutine


    function getState(self) result(state)
        implicit none 
        class(Circuit),intent(inout)::self
        complex*16::state(self%d) 
        ! ---------------------------
        state = self%s
    endfunction

    subroutine U2(self,i,U)
        implicit none
        class(Circuit),intent(inout)::self
        integer*8,intent(in)::i 
        complex*16,intent(in)::U(2,2) 
        ! ----------------------
        complex*16::tmpS(0:self%d-1),a,b 
        integer*8::w ,w0,w1 
        tmpS = (0._8,0._8) 
        Do w = 0, self%d-1_8 
            ! write(*,*)w,i,999965
            w0 = ibclr( w , i )
            w1 = ibset( w , i ) 
            if (btest( w,i )) then
                a = U(1,2) 
                b = U(2,2)
            else 
                a = U(1,1) 
                b = U(2,1)
            endif 
            tmpS(w0) = tmpS(w0) + a * self%s(w) 
            tmpS(w1) = tmpS(w1) + b * self%s(w)  
        enddo
        self%s = tmps 
    endsubroutine

    subroutine U4(self,i,j,U)
        implicit none
        class(Circuit),intent(inout)::self
        integer*8,intent(in)::i,j 
        complex*16,intent(in)::U(4,4) 
        ! ----------------------
        complex*16::tmpS(0:self%d-1) 
        integer*8::II,IA,IB,w 
        tmpS = (0._8,0._8) 
        Do w = 0, self%d-1_8
            if (btest(w,i)) then 
                IA = 1_8 
            else 
                IA = 0_8 
            endif
            if (btest(w,j)) then 
                IB = 1_8
            else
                IB = 0_8 
            endif  
            II = IA * 2 + IB + 1_8 
            IA = ibclr(ibclr(w,i),j); tmpS(IA) = tmpS(IA) + U(1,II) * self%s(w) 
            IA = ibset(ibclr(w,i),j); tmps(IA) = tmps(IA) + U(2,II) * self%s(w) 
            IA = ibclr(ibset(w,i),j); tmps(IA) = tmps(IA) + U(3,II) * self%s(w)
            IA = ibset(ibset(w,i),j); tmps(IA) = tmps(IA) + U(4,II) * self%s(w)    
        enddo
        self%s = tmps 
    endsubroutine

    subroutine runWithGatesFile(self,fileName)
        implicit none
        class(Circuit),intent(inout)::self
        character(*),intent(in)::fileName
        ! ---------------------------------
        integer*8::N_gate,gid,Nu,i,j,qi,qj  
        real*8::rp,ip 
        complex*16::U2(2,2),U4(4,4)
        open(999,file=fileName,form='FORMATTED')
        ! read(999)N_gate
        
        do while (.True.)
            read(999,*)Nu
            ! write(*,*)9995,Nu
            if ( Nu .eq. 1_8 ) then
                ! 1 qubit gate
                read(999,*)qi 
                do i = 1_8,2_8
                    do j = 1_8,2_8 
                        read(999,*)rp 
                        read(999,*)ip 
                        U2(i,j) = rp + ip*(0._8,1._8) 
                    enddo  
                enddo
                call self%OneQubitGate(qi,U2) 
            elseif (Nu.eq.2_8) then 
                !  2 qubit gate
                read(999,*)qi 
                read(999,*)qj
                ! write(*,*)Nu,666,qi,qj
                do i = 1_8,4_8
                    do j = 1_8,4_8 
                        read(999,*)rp 
                        read(999,*)ip 
                        U4(i,j) = rp + ip*(0._8,1._8) 
                    enddo  
                enddo
                ! write(*,*)U4,999
                call self%TwoQubitGate(qi,qj,U4)
                ! write(*,*)"here2222"
            elseif (Nu.eq.-1_8) then 
                goto 9999
            endif  
        enddo 
   9999 continue
        close(999)
    endsubroutine

    subroutine stdoutMeasurement(self) 
        implicit none
        class(Circuit),intent(inout)::self
        ! ----------------------------
        integer*8::i 
        complex*16::v
        do i = 0_8,self%d-1
            v = self%s(i)
            write(*,"(F16.14)") real( v * conjg(v) ) 
        enddo 
    endsubroutine


end module



program name
    use mod_Circuit, only: Circuit 
    implicit none

    character(len=256)::arg
    type(Circuit)::C
    integer::val_i,i  
    character(len=256)::val_gatePath

    i = 1
    call get_command_argument(i, arg)
    read(arg,*)val_i
    

    i = 2 
    call get_command_argument(i, arg)
    read(arg,*) val_gatePath
    val_gatePath = trim(adjustl(val_gatePath))

    ! write(*,*)"input file = ",val_gatePath

    call c%Initialization( 1_8 * val_i )
    call c%runWithGatesFile( val_gatePath ) 
    call c%stdoutMeasurement()

end program name